from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
from pypdf import PdfReader
from docx import Document
import re
from app.embeddings import generate_embeddings
from app.vector_store import create_collection, store_chunks
from app.chunker import split_text

app = FastAPI(title="AI Document & Compliance Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/") # main endpoint
async def root():
    return {
        "message": "AI Document & Compliance Assistant API is running"
    }

@app.post("/documents") # documents upload endpoint
async def upload_document(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
        return {"error":"Content type not supported"}
    
    os.makedirs("uploads", exist_ok = True)
    
    # save the file as is
    with open(f"uploads/{file.filename}", "wb") as buffer:
        buffer.write(await file.read())

    # read the saved file
    try:
        file_data = extract_text(file)
    except Exception as e:
        return {"error": str(e)}

    # clean the text
    cleaned_text = clean_text(file_data)

    #chunking
    chunked_text = split_text(cleaned_text)

    # make embeddings
    embedded_text = generate_embeddings(chunked_text)

    #store it in Qdrant via a docker
    create_collection()
    store_chunks(chunked_text, embedded_text)

    return {
        "message": "Document uploaded and indexed successfully",
        "filename": file.filename,
        "chunks": len(chunked_text)
    }

def extract_text_from_pdf(file_path): # extracts pdfs into normal string format
    pdf = PdfReader(file_path)

    full_text = ""

    for page in pdf.pages:
        full_text += page.extract_text() + "\n"

    return full_text

def extract_text_from_docx(file_path): # extracts docx into string format
    doc = Document(file_path)

    full_text = ""
    for paragraph in doc.paragraphs:
        full_text += paragraph.text + "\n"
    
    return full_text

def extract_text_from_txt(file_path): # extracts txt into string
    with open(file_path, "r", encoding = "utf-8") as file:
        return file.read()

def extract_text(file): # determines how the file should be extracted
    match file.content_type:
        case "application/pdf":
            return extract_text_from_pdf(f"./uploads/{file.filename}")
        case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return extract_text_from_docx(f"./uploads/{file.filename}")
        case "text/plain":
            return extract_text_from_txt(f"./uploads/{file.filename}")
        case _:
            return {"error": "file type not supported"}

def clean_text(full_text): # removes whitespaces, excessive spaces and tabs
    text = full_text.strip()
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = re.sub(r"[ \t]+",  " ", text)

    return text
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os, re
from docx import Document
from app.embeddings import generate_embeddings
from app.vector_store import create_collection, store_chunks
from app.chunker import split_text
from app.boilerplate import extract_clean_pages
from uuid import uuid4
import pymupdf

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

    # clean the text of each page
    cleaned_pages = clean_pages(file_data)

    #chunking
    chunked_text = split_text(cleaned_pages)

    # make embeddings
    embedded_text = generate_embeddings(chunked_text)

    #store it in Qdrant via a docker
    document_id = str(uuid4())

    create_collection()
    store_chunks(chunked_text, embedded_text, document_id, file.filename)

    return {
        "message": "Document uploaded and indexed successfully",
        "filename": file.filename,
        "chunks": len(chunked_text)
    }

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF while preserving page numbers.

    Parameters:
        file_path (str): Path to the PDF file.

    Returns:
        list[dict]: Page numbers and extracted text for each page.
    """
    document = pymupdf.open(file_path)
    pages = []
    for  page_number, page in enumerate(document):
        text = page.get_text("text", sort = True).strip()

        if not text:
            continue

        # separate table of content pages for reports
        first_lines = text.splitlines()[0] if text.strip() else ""
        first_words = first_lines.split()[:3]
        heading = " ".join(word.strip().lower() for word in first_words)
        if heading.startswith("table of contents"):
            continue
        if heading.startswith("contents"):
            continue
        if heading.startswith("table of figures"):
            continue

        pages.append({"page_number": page_number+1, "text": text})
    document.close()
    return pages

def extract_text_from_docx(file_path):
    """
    Extracts text from a DOCX file.

    Parameters:
        file_path (str): Path to the DOCX file.

    Returns:
        str: Extracted text from the document.
    """
    doc = Document(file_path)

    full_text = ""
    for paragraph in doc.paragraphs:
        full_text += paragraph.text + "\n"
    
    return full_text

def extract_text_from_txt(file_path):
    """
    Extracts text from a TXT file.

    Parameters:
        file_path (str): Path to the TXT file.

    Returns:
        str: Text contained in the file.
    """
    with open(file_path, "r", encoding = "utf-8") as file:
        return file.read()

def extract_text(file):
    """
    Determines the appropriate extraction method based on file type.

    Parameters:
        file: Uploaded file.

    Returns:
        The extracted content from the appropriate extraction function,
        or an error message for unsupported file types.
    """
    match file.content_type:
        case "application/pdf":
            return extract_clean_pages(f"./uploads/{file.filename}")
        case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return {"error": "file type not supported yet"}
        case "text/plain":
            return {"error": "file type not supported yet"}
        case _:
            return {"error": "file type not supported"}

def clean_pages(pages):
    """
    Performs basic text cleaning on each page

    Parameters:
        pages (list[dict]): Pages containing dictionary and text

    Returns:
        list[dict]: Cleaned text from each page with their page number
    """
    cleaned_pages = []
    for page in pages:
        text = page["text"].strip()
        text = re.sub(r"\n\s*\n+", "\n\n", text)
        text = re.sub(r"[ \t]+",  " ", text)

        if text:
            cleaned_pages.append({
                "page_number": page["page_number"], "text": text
            })
    
    return cleaned_pages
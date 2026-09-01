from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
from pypdf import PdfReader

app = FastAPI(title="AI Document & Compliance Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/")
async def root():
    return {
        "message": "AI Document & Compliance Assistant API is running"
    }

@app.post("/documents")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
        return {"error":"Content type not supported"}
    
    os.makedirs("uploads", exist_ok = True)

    with open(f"uploads/{file.filename}", "wb") as buffer:
        buffer.write(await file.read())

def extract_text_from_pdf(file_path):
    pdf = PDFReader
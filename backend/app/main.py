import os
import io
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="AI Text Summarizer API")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
# Using Facebook's BART model which is excellent for summarization and free on the Inference API
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

class SummarizeRequest(BaseModel):
    text: str

def generate_summary(text: str) -> str:
    """Helper function to call Hugging Face API for summarization."""
    if not HF_API_KEY:
        return "Error: HUGGINGFACE_API_KEY is not set in the environment variables. Please add it to your .env file."
        
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": text,
        "parameters": {"max_length": 250, "min_length": 50, "do_sample": False}
    }
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        
        # Check if the model is still loading (Status 503)
        if response.status_code == 503:
            raise HTTPException(
                status_code=503, 
                detail="The Hugging Face model is currently loading into memory. Please wait about 30 seconds and try again."
            )
            
        response.raise_for_status()
        result = response.json()
        
        # Hugging Face returns a list with a dictionary containing 'summary_text'
        if isinstance(result, list) and len(result) > 0 and "summary_text" in result[0]:
            return result[0]["summary_text"]
        else:
            return f"Unexpected response format from Hugging Face: {result}"
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Hugging Face API Error: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Text Summarizer API"}

@app.post("/api/summarize/text")
def summarize_text(request: SummarizeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    summary = generate_summary(request.text)
    return {"summary": summary}

@app.post("/api/summarize/pdf")
async def summarize_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    try:
        # Read the file content into memory
        contents = await file.read()
        pdf_reader = PdfReader(io.BytesIO(contents))
        
        # Extract text from all pages
        extracted_text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"
            
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF. It might be scanned or empty.")
            
        # Truncate text if it's too long (BART model limit is roughly 1024 tokens ~ 4000 characters)
        max_chars = 4000
        if len(extracted_text) > max_chars:
            extracted_text = extracted_text[:max_chars]
            
        summary = generate_summary(extracted_text)
        
        return {
            "summary": summary,
            "extracted_words": len(extracted_text.split())
        }
    except Exception as e:
        # Avoid overriding Hugging Face 503 errors
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

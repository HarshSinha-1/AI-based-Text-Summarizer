import os
import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PyPDF2 import PdfReader
from openai import OpenAI
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

# Initialize OpenAI Client (Requires OPENAI_API_KEY in .env)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SummarizeRequest(BaseModel):
    text: str

def generate_summary(text: str) -> str:
    """Helper function to call OpenAI API for summarization."""
    if not os.getenv("OPENAI_API_KEY"):
        return "Error: OPENAI_API_KEY is not set in the environment variables. Please add it to your .env file."
        
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a highly capable AI assistant that summarizes text concisely. Keep the summary structured and easy to read."},
                {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
            ],
            max_tokens=500,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")

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
            
        # Truncate text if it's too long (Basic handling to avoid exceeding token limits)
        max_chars = 12000 # Roughly 3000-4000 tokens
        if len(extracted_text) > max_chars:
            extracted_text = extracted_text[:max_chars] + "\n...[Text truncated due to length limitations]"
            
        summary = generate_summary(extracted_text)
        
        return {
            "summary": summary,
            "extracted_words": len(extracted_text.split())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

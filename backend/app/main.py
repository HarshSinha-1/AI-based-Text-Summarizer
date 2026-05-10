from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="AI Text Summarizer API")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummarizeRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Text Summarizer API"}

@app.post("/api/summarize/text")
def summarize_text(request: SummarizeRequest):
    # TODO: Implement AI summarization
    # For now, return a placeholder functional response
    return {"summary": f"Placeholder summary for: {request.text[:50]}..."}

@app.post("/api/summarize/pdf")
def summarize_pdf():
    # TODO: Implement PDF text extraction and summarization
    return {"summary": "Placeholder summary for PDF content"}

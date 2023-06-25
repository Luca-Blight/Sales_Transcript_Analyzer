

import os 
import pdfplumber

from fastapi import APIRouter
from pydantic import BaseModel
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from dotenv import load_dotenv,find_dotenv

router = APIRouter()

class DocumentRequest(BaseModel):
    document: str

@router.post("/analyze")
def analyze_document(request: DocumentRequest):
    document = request.document
    
    # Process the document using the language model
    insights = process_document(document)
    
    # Return the insights to the user
    return insights

def process_document(document: str):
    # Logic to process the document using the language model
    # Replace this with your actual LLM implementation
    
    # Example dummy insights
    insights = {
        "word_count": len(document.split()),
        "sentence_count": document.count("."),
        # Add more insights as needed
    }
    
    return insights

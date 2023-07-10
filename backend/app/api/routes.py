import asyncio
import os
import time
import openai

from fastapi import APIRouter, UploadFile
from fastapi.responses import HTMLResponse
from langchain.chat_models import ChatOpenAI
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv, find_dotenv
from .prompts import product_prompt_template, final_product_prompt_template
from utils.document_utils import extract_text_from_pdf, split_into_chunks
from rich import print

import guardrails as gd

_ = load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>My Cool FastAPI App</title>
            <style>
                body {
                    background-color: lightblue;
                }
                h1 {
                    color: white;
                    text-align: center;
                    padding-top: 50px;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to my FastAPI app!</h1>
        </body>
    </html>
    """


@router.post("/analyze")
async def analyze_document(file: UploadFile) -> dict:
    start = time.time()
    filename = file.filename
    loop = asyncio.get_event_loop()

    with ThreadPoolExecutor() as executor:
        if filename.endswith(".pdf"):
            extracted_text = await loop.run_in_executor(
                executor, extract_text_from_pdf, file.file
            )

            guard = gd.Guard.from_rail('/Users/Zachary_Royals/Code/zelta-challenge/backend/app/api/sales_transcript.rail')
            
            chunks = await loop.run_in_executor(
                executor, split_into_chunks, extracted_text
            )
            # run tasks in parallel
            for chunk in chunks:
                raw_llm_output, validated_output = guard(
                                                    openai.ChatCompletion.create,
                                                    prompt_params={"sales_transcript": chunk},
                                                    engine="chat-gpt4",
                                                    max_tokens=1024,
                                                    temperature=0.3,
                                                    
                                            )
                
            execution_time = time.time() - start
            print(f'Time taken: {execution_time} seconds')
            return validated_output

        elif file.endswith(".txt"):
            return "This is a text file."
        else:
            return "Error: This is not a PDF or text file."

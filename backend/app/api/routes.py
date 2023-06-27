import asyncio
import os
import tempfile

from fastapi import APIRouter, UploadFile
from fastapi.responses import HTMLResponse
from langchain.chat_models import ChatOpenAI
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv, find_dotenv
from prompts import product_prompt_template, final_product_prompt_template
from utils.document_utils import extract_text_from_pdf, split_into_chunks


_ = load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

router = APIRouter()


# class Document(BaseModel):
#     file: UploadFile = File()


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


@router.post("/analyze/")
async def analyze_document(file: UploadFile) -> dict:
    filename = file.filename

    loop = asyncio.get_event_loop()

    with ThreadPoolExecutor() as executor:
        if filename.endswith(".pdf"):
            # run blocking operations in a thread pool

            pdf_bytes = await file.read()  # read file into bytes

            # write bytes to a temporary file
            temp_pdf_file = tempfile.NamedTemporaryFile(delete=False)
            temp_pdf_file.write(pdf_bytes)

            extracted_text = await loop.run_in_executor(
                executor, extract_text_from_pdf, temp_pdf_file.name
            )
            temp_pdf_file.close()

            os.unlink(temp_pdf_file.name)

            chunks = await loop.run_in_executor(
                executor, split_into_chunks, extracted_text
            )

            insights = []

            for chunk in chunks:
                transcript = product_prompt_template.format_messages(text=chunk)
                chat = ChatOpenAI(temperature=0.0, model="gpt-4")
                # run blocking operations in a thread pool
                insight = await loop.run_in_executor(executor, chat, transcript)
                insights.append(insight)

            summary = final_product_prompt_template.format_messages(text=insights)
            chat = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo-16k")
            # run blocking operations in a thread pool
            final_insights = await loop.run_in_executor(executor, chat, summary)

            return final_insights

        elif file.endswith(".txt"):
            return "This is a text file."
        else:
            return "Error: This is not a PDF or text file."

import asyncio
import os

from PyPDF2 import PdfReader

from fastapi import APIRouter
from pydantic import BaseModel
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv, find_dotenv

from prompts import product_prompt_template,final_product_prompt_template

_ = load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    return text


def split_into_chunks(text: str) -> list[str]:
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=12000, chunk_overlap=1200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


async def analyze_document(document: str) -> dict:
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        if document.endswith(".pdf"):
                # run blocking operations in a thread pool
            extracted_text = await loop.run_in_executor(executor, extract_text_from_pdf, document)
            chunks = await loop.run_in_executor(executor, split_into_chunks, extracted_text)
            
            insights = []
            
            for chunk in chunks:
                transcript = product_prompt_template.format_messages(text=chunk)
                chat = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo-16k")
                # run blocking operations in a thread pool
                insight = await loop.run_in_executor(executor, chat, transcript)
                insights.append(insight)

            summary = final_product_prompt_template.format_messages(text=insights)
            chat = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo-16k")
            # run blocking operations in a thread pool
            final_insights = await loop.run_in_executor(executor, chat, summary)
            return final_insights

 
        elif document.endswith(".txt"):
            return "This is a text file."
        else:
            return "Error: This is not a PDF or text file."


# Now you can call this async function in an event loop.
# Here's a basic example of how you might do it:

async def main():
    # Assume 'document.pdf' is the path to a PDF file
    document = '/Users/Zachary_Royals/Code/zelta-challenge/Sample Transcript_pdf.pdf'
    results = await analyze_document(document)
    print(results)

# Run the event loop
asyncio.run(main())

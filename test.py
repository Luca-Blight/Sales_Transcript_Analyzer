import os

from PyPDF2 import PdfReader

from fastapi import APIRouter
from pydantic import BaseModel
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv, find_dotenv

from prompts import product_prompt_template

_ = load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def extract_text_from_pdf(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    return text


def split_into_chunks(text: str) -> list[str]:
    """Splits text into chunks

    Args:
        text (_type_): _extracted text_

    Returns:
        _type_: _description_
    """
    text_splitter = CharacterTextSplitter(
        seperator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_into_chunks(text)
    return chunks


def create_embeddings(chunks):
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    return knowledge_base


def analyze_document(document: str) -> dict:
    if document.endswith(".pdf"):
        try:
            extracted_text = extract_text_from_pdf(document)
            messages = product_prompt_template.format_messages(text=extracted_text)
            chat = ChatOpenAI(temperature=0.0)
            insights = chat(messages)
            breakpoint()
            return insights.content
            # chunks = split_into_chunks(extracted_text)
            # knowledge_base = create_embeddings(chunks)

            return insights

        except Exception as e:
            print("Error: ", e)
    elif document.endswith(".txt"):
        return "This is a text file."
    else:
        return "Error: This is not a PDF or text file."

    # Return the insights to the user


def process_document(document):
    # Logic to process the document using the language model
    # Replace this with your actual LLM implementation

    # Example dummy insights
    breakpoint()
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    insights = {
        "word_count": len(document.split()),
        "sentence_count": document.count("."),
    }
    # Add more insights as needed-

    return insights


result = analyze_document(
    "/Users/Zachary_Royals/Code/zelta-challenge/Sample Transcript_pdf.pdf"
)


# insights = knowledge_base.similarity_search("This is a test")
# chain_type_kwargs = {"prompt": prompt}
# chain = RetrievalQAWithSourcesChain.from_chain_type(
#     llm,
#     chain_type="stuff",
#     retriever=vectorstore_mydocs.as_retriever(),
#     chain_type_kwargs=chain_type_kwargs
# )

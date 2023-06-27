
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader

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

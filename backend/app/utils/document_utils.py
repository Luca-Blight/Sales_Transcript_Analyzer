
from langchain.text_splitter import CharacterTextSplitter
# from PyPDF2 import PdfReader
import pdfplumber
from nltk.tokenize import word_tokenize, sent_tokenize

def extract_text_from_pdf(pdf):
    with pdfplumber.open(pdf) as pdf_reader:
        text = "\n".join(page.extract_text() for page in pdf_reader.pages)
    return text


def split_into_chunks(text: str) -> list[str]:
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=12000, chunk_overlap=1200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks
# def split_into_chunks(text: str, max_token_count: int=7000) -> list[str]:
#     sentences = sent_tokenize(text)
#     chunks = []
#     current_chunk = ''
#     current_token_count = 0

#     for sentence in sentences:
#         tokens = word_tokenize(sentence)
#         if current_token_count + len(tokens) > max_token_count:
#             chunks.append(current_chunk)
#             current_chunk = sentence
#             current_token_count = len(tokens)
#         else:
#             current_chunk += ' ' + sentence
#             current_token_count += len(tokens)

#     if current_chunk:
#         chunks.append(current_chunk)
#     return chunks

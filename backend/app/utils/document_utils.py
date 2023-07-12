
from langchain.text_splitter import CharacterTextSplitter
import pdfplumber
# from PyPDF2 import PdfReader

from nltk.tokenize import word_tokenize, sent_tokenize

def extract_text_from_pdf(pdf) -> str:
    with pdfplumber.open(pdf) as pdf_reader:
        text = "\n".join(page.extract_text() for page in pdf_reader.pages)
    return text


def split_into_chunks(text: str, chunk_size: int=6000, chunk_overlap: int=400) -> list[str]:

    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )
    chunks = text_splitter.split_text(text)
    print(f'There are {len(chunks)} chunks with a chunk size of {chunk_size} and an overlap size of {chunk_overlap}')
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

from langchain.text_splitter import CharacterTextSplitter
import pdfplumber


def extract_text_from_pdf(pdf) -> str:
    with pdfplumber.open(pdf) as pdf_reader:
        text = "\n".join(page.extract_text() for page in pdf_reader.pages)
    return text


def split_into_chunks(
    text: str, chunk_size: int = 6000, chunk_overlap: int = 400
) -> list[str]:

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    print(
        f"There are {len(chunks)} chunks with a chunk size of {chunk_size} and an overlap size of {chunk_overlap}"
    )
    return chunks

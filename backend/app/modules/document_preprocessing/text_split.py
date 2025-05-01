from .extract_pdf import PDFExtraction
from typing import List
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter



def split_text(pdf_docs: List[str], chunk_size: int = 100, chunk_overlap: int = 20) -> List[Document]:
    """
    Splits text into chunks for efficient embedding.
    
    - `chunk_size`: Max characters per chunk.
    - `chunk_overlap`: Overlap between chunks for better context retention.
    
    Returns a list of text chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    chunks = []
    for page_text in pdf_docs:
        split_chunks = text_splitter.split_text(page_text)
        for chunk in split_chunks:
            chunks.append(Document(page_content=chunk))
    
    return chunks



if __name__ == "__main__":
    
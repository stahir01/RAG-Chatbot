import json
import os
from typing import List
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .extract_and_clean_pdf import PDFExtraction, CleanText
from backend.app.config import PROJECT_ROOT



def split_text(
        pdf_docs: List[str], 
        chunk_size: int = 1000, 
        chunk_overlap: int = 200) -> List[Document]:
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


if __name__ == '__main__':
    pdf_path = os.path.join(PROJECT_ROOT, "documents", "Guideline_atraumatische_Femurkopfnekrose_2019-09_1-abgelaufen.pdf")
    
    pdf_extractor = PDFExtraction()
    raw_text = pdf_extractor.extract_text_from_pdf(pdf_path)
    
    if isinstance(raw_text, list):
        raw_text = "\n".join(raw_text)
        
    cleaner = CleanText(raw_text)
    cleaned_text = cleaner.clean()
    
    
    text_chunks = split_text([cleaned_text], chunk_size=1000, chunk_overlap=200)
    with open("text_chunks.json", "w") as f:
        json.dump([doc.page_content for doc in text_chunks], f, indent=4)
    print(f"Extracted {len(text_chunks)} text chunks.")
    
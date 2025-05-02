import os
import logging
from typing import List, Optional
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from backend.app.modules.document_preprocessing import PDFExtraction, CleanText, split_text
from backend.app.config import (
    OPENAI_KEY,
    MINI_LM_EMBED,
    OPENAI_EMBED,
    VECTOR_DB_PATH,
    PROJECT_ROOT
)
DEFAULT_EMBED_MODEL = MINI_LM_EMBED 


def store_embeddings(
        docs: List[Document],
        embed_model: Optional[str] = None,
        collection_name: str = "chromadb"
    ) -> None:

    """
    Generates embeddings for text chunks and stores them in ChromaDB.

    Args:
        docs (List[Document]): List of documents to embed.
        embed_model (Optional[str]): Name of the embedding model.  Defaults to OPENAI_EMBED.
        collection_name (str): Name of the ChromaDB collection.  Defaults to "chromadb".
    """

    if embed_model is None:
        embed_model = OPENAI_EMBED

    logging.info(f"Using embedding model: {embed_model}") 

    if embed_model == OPENAI_EMBED:
        embedding_model = OpenAIEmbeddings(model=OPENAI_EMBED, api_key=OPENAI_KEY)
    elif embed_model == MINI_LM_EMBED:
        embedding_model = HuggingFaceEmbeddings(model_name=MINI_LM_EMBED)
    else:
        raise ValueError(f"Unsupported embedding model: {embed_model}") 
    
    text_chunks = [doc.page_content for doc in docs]
    metadata = [doc.metadata for doc in docs]
    logging.info(f"Number of chunks to embed: {len(text_chunks)}") 

    dir_path = os.path.join(VECTOR_DB_PATH, collection_name)
    os.makedirs(dir_path, exist_ok=True)
    logging.info(f"ChromaDB directory: {dir_path}")

    db = Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model, 
        persist_directory=dir_path
    )
    db.aadd_texts(texts=text_chunks, metadatas=metadata) 

    logging.info(f"✅ Stored {len(text_chunks)} text chunks in ChromaDB (Collection: {collection_name})")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) 
    pdf_path = os.path.join(PROJECT_ROOT, "documents", "Guideline_atraumatische_Femurkopfnekrose_2019-09_1-abgelaufen.pdf")
    
    pdf_extractor = PDFExtraction()
    raw_text = pdf_extractor.extract_text_from_pdf(pdf_path)
    
    if isinstance(raw_text, list):
        raw_text = "\n".join(raw_text)
        
    cleaner = CleanText(raw_text)
    cleaned_text = cleaner.clean()
    text_chunks = split_text(cleaned_text, chunk_size=1000, chunk_overlap=200)
    print(f"Extracted {len(text_chunks)} text chunks.")

    store_embeddings(text_chunks, embed_model=OPENAI_EMBED, collection_name="medical_dataset")
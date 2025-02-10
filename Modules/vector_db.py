import os
import logging
from typing import List, Optional
from time import sleep
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from .data_loader import *

#Variables
EMBED_DELAY = 0.2  # 20 miliseconds
#MISTRAL_MODEL = 'Linq-AI-Research/Linq-Embed-Mistral' #Too big to download
MINI_LM = 'sentence-transformers/all-MiniLM-L6-v2'


def split_documents_into_chunks(
            pdf_path: str= None, 
            json_path: str= None, 
            chunk_size: int = 500, 
            chunk_overlap: int = 0 
        ) -> List[Document]:
    
    """Splits a list of documents or raw text content into smaller chunks."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunked_docs = []

    if pdf_path is not None:
        pdf_doc = load_pdf(pdf_path)
        for doc in pdf_doc:
            chunks = text_splitter.split_text(doc["text"])
            for chunk in chunks:
                chunked_docs.append(Document(page_content=chunk, metadata={"page": doc["page"]}))
        logging.info(f"Successfully split PDF into {len(chunked_docs)} chunks.")

    if json_path is not None:
        json_docs = load_json(json_path)
        for doc in json_docs:
            chunks = text_splitter.split_text(doc["text"])
            for chunk in chunks:
                chunked_docs.append(Document(page_content=chunk, metadata={"page": doc["page"], "section": doc.get("section", "N/A")}))
        logging.info(f"Successfully split JSON into {len(chunked_docs)} chunks.")

    return chunked_docs


def create_vector_db(
    documents: List[Document],
    embeddings: Optional[HuggingFaceEmbeddings] = None,
    collection_name: str = "chroma_db",
    persist_directory: str = "vector_store"
) -> Chroma:
    """
    Creates a vector database and adds text documents to it.

    Args:
        documents (List[Document]): The documents to be stored.
        embeddings (Optional[HuggingFaceEmbeddings]): The embedding model to use. If not provided, a default embedding model is used.
        collection_name (str): The name of the Chroma collection.
        persist_directory (str): The directory where the database is persisted.

    Returns:
        Chroma: The vector database instance containing the added documents.
    """
    if not documents:
        logging.warning("No documents provided to create a vector database.")
        return None

    # Use provided embeddings or a default model
    if embeddings is None:
        embeddings = HuggingFaceEmbeddings(model_name=MINI_LM)
    
    texts = [doc.page_content for doc in documents]
    metadata = [doc.metadata for doc in documents]
    
    persist_path = os.path.join(persist_directory, collection_name)

    # Create and initialize the Chroma vector database
    db = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_path
    )

    db.add_texts(texts, metadatas=metadata)
    db.persist()
    
    logging.info(f"Vector database '{collection_name}' created with {len(texts)} documents.")

    return db





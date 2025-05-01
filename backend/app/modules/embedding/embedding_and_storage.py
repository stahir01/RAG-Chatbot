import os 
from typing import List, Optional
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from backend.app.config import (
    OPENAI_KEY,
    MINI_LM_EMBED,
    OPENAI_EMBED,
    VECTOR_DB_PATH
)



def store_openai_embeddings(
        docs: List[Document],
        embed_model: Optional[str] = None,
        collection_name: str = "chromadb"
    ) -> None:

    """
    Generates embeddings for text chunks and stores them in ChromaDB.

    Args:
        docs (List[Document]): List of documents to embed.
        embed_model (Optional[str]): Name of the Hugging Face embedding model.
        collection_name (str): Name of the ChromaDB collection.
    """

    if embed_model is None:
        embed_model = OPENAI_EMBED

    embedding_model = OpenAIEmbeddings(model=embed_model, api_key=OPENAI_KEY)

    text_chunks = [doc.page_content for doc in docs]
    metadata = [doc.metadata for doc in docs]

    dir_path = os.path.join(VECTOR_DB_PATH, collection_name)
    os.makedirs(dir_path, exist_ok=True)

    db = Chroma(
        collection_name=collection_name,
        persist_directory=dir_path,
        embedding_function=embedding_model  
    )

    db.add_texts(texts=text_chunks, metadatas=metadata, embeddings=embedding_model)


    logging.info(f"✅ Stored {len(text_chunks)} text chunks in ChromaDB (Collection: {collection_name})")
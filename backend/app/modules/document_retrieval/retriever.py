import os
import logging
from rouge_score import rouge_scorer
from typing import List, Optional
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from backend.app.config import (
    OPENAI_KEY,
    OPENAI_EMBED,
    VECTOR_DB_PATH
)
DEFAULT_EMBED_MODEL = OPENAI_EMBED

def retrieve_text(
        vectordb_path: str,
        query: str,
        embed_model: Optional[str] = None,
        collection_name: str = "chromadb",
        results_to_return: int = 3):
    """
    Retrieve text from the vector store based on the query.

    Args:
        vector_db (Chroma): ChromaDB instance.
        query (str): Query string to search for in the vector store.

    Returns:
        List[Document]: Retrieved documents from the vector store.
    """
    if not os.path.exists(vectordb_path):
        raise FileNotFoundError(f"Vector store not found at: {vectordb_path}")

    if not query:
        raise ValueError("Query cannot be empty.")

    if embed_model is None:
        embed_model = DEFAULT_EMBED_MODEL

    embedding_model = OpenAIEmbeddings(model=embed_model, api_key=OPENAI_KEY)

    print(f"Retrieving from Vector DB Path: {vectordb_path}")
    vector_db = Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model,
        persist_directory=vectordb_path
    )

    matched_texts = vector_db.similarity_search_with_score(query, k=results_to_return)

    print(f"Number of Retrieved Texts: {len(matched_texts)}")
    print(f"Query used for retrieval: {query}")

    return matched_texts


if __name__ == "__main__":
    vectordb_path = os.path.join(VECTOR_DB_PATH, "medical_dataset")
    question = "weiterführende Bildgebung ist indiziert bei persistierenden Hüftschmerzen über 6 Wochen trotz unauffälligem Röntgenbefund?"
    answer_reference = ["MRT bei persistierenden Beschwerden mit unauffälligem Röntgenbefund"] 

    matched_texts = retrieve_text(
        vectordb_path=vectordb_path,
        query=question,
        embed_model=OPENAI_EMBED,
        collection_name="medical_dataset",
        results_to_return=3
    )

    retrieved_docs = [doc.page_content for doc, _ in matched_texts]
    reference_text = answer_reference[0]

    print("\n=== Ground Truth ===")
    print(reference_text)
    print("\n=== Retrieved Texts ===")
    for i, (doc, chroma_score) in enumerate(matched_texts):
        text = doc.page_content
        print(f"Text {i+1} (Score: {chroma_score:.3f}):\n{text}\n---")

    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
    print("\n=== ROUGE Scores ===")
    all_scores = []
    for i, text in enumerate(retrieved_docs):
        scores = scorer.score(reference_text, text)
        all_scores.append(scores)
        
        print(f"\nText {i+1} Scores:")
        for metric in ['rouge1', 'rouge2', 'rougeL']:
            print(f"{metric}:")
            print(f"  Precision: {scores[metric].precision:.3f}")
            print(f"  Recall:    {scores[metric].recall:.3f}")
            print(f"  F1:        {scores[metric].fmeasure:.3f}")
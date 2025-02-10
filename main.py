from dotenv import load_dotenv
from fastapi import FastAPI, Query
import logging
from Modules import *

load_dotenv()
HUGGING_FACE_Key = os.getenv('HUGGINGFACE_Key')

app = FastAPI()

# Global variables
db = None
llm = None

@app.on_event("startup")
def initialize_system():
    """
    Initializes the vector store and language model before handling requests.
    """
    global db, llm
    
    # Load the language model
    llm = get_model(HUGGING_FACE_Key)
    
    # Process documents into vector embeddings
    chunked_docs = split_documents_into_chunks(
        pdf_path='documents/rag_wiki.pdf',
        json_path='documents/attention_wiki.json',
        chunk_size=500,
        chunk_overlap=20
    )
    
    db = create_vector_db(chunked_docs)
    logging.info("Vector store initialized with documents!")

@app.get("/query")
def query(question: str = Query(..., description="Your query")):
    """
    Handles user queries by retrieving relevant documents and generating responses.
    """
    if db is None:
        return {"error": "Vector store is not initialized!"}
    
    return answer_question(question, llm, db)

@app.get("/")
def home():
    """
    Root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the RAG System API! Use /query to ask questions."}

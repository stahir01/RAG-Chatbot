from dotenv import load_dotenv
from fastapi import FastAPI, Query

from Modules import *

load_dotenv()
HUGGING_FACE_Key = os.getenv('HUGGINGFACE_Key')

app = FastAPI()

#global var
db = None  
llm = None 

@app.on_event("startup")
def setup():
    """
    Ensures vector store and model are initialized before requests.
    """
    global db, llm
    llm = get_model(HUGGING_FACE_Key)

    # Extract & chunk documents before creating vector database
    chunked_docs = split_documents_into_chunks (
        pdf_path='documents/rag_wiki.pdf',
        json_path='documents/attention_wiki.json',
        chunk_size=500,
        chunk_overlap=20
    )
    chunked_docs
    # Create vector database
    db = create_vector_db(chunked_docs)
    logging.info("Vector store initialized with documents!")

@app.get("/query")
def query(question: str = Query(..., description="Your query")):
    if db is None:
        return {"error": "Vector store is not initialized!"}
    
    return answer_question(question, llm, db)


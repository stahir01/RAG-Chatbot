import os
from langchain_community.llms import HuggingFaceEndpoint 
from langchain.vectorstores  import Chroma
from dotenv import load_dotenv

load_dotenv()

HUGGING_FACE_Key = os.getenv('HUGGINGFACE_Key')
DEEPSEEK_MODEL = 'deepseek-ai/DeepSeek-R1-Distill-Llama-70B'
#LLAMA_MODEL_70B = 'meta-llama/Llama-2-70b-chat-hf'
#MISTRAL_MODEL = 'mistralai/Mistral-Large-Instruct-2407'



def get_model(api_token: str) -> HuggingFaceEndpoint:
    """
    Initializes and returns a Hugging Face LLM model for text generation.

    Args:
        api_token (str): Hugging Face API token.

    Returns:
        ChatHuggingFace: A chat-ready model instance.
    """
    llm = HuggingFaceEndpoint(
        repo_id=DEEPSEEK_MODEL,
        task="text-generation",
        max_new_tokens=500,
        do_sample=False,
        top_k=3,
        temperature=0.1,
        huggingfacehub_api_token=api_token,
    )
    return llm


def answer_question(
        question: str, 
        model: HuggingFaceEndpoint,
        vector_db: str
    ) -> dict:
    """
    Retrieves relevant context from ChromaDB and uses the LLM to answer the question.

    Args:
        question (str): The user's query.
        model (HuggingFaceEndpoint): The initialized Hugging Face model.

    Returns:
        dict: The answer along with metadata.
    """
    if vector_db is None:
        return {"error": "Vector store not initialized!"}
    
    docs = vector_db.similarity_search(question, k=3)

    if not docs:
        return {
            "answer": "No relevant answer found.",
            "Page number": "N/A",
            "Additional Metadata": "None"
        }

    # Combine retrieved context
    context = "\n".join([doc.page_content for doc in docs])
    metadata = docs[0].metadata  # Get metadata from the most relevant document

    # Construct LLM prompt
    prompt = f"""
    You are an AI assistant with access to specific documents.
    Use only the following context to answer the question.
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:
    """
    
    # Generate answer using the LLM
    answer = model.invoke(prompt)

    return {
        "answer": answer.strip(),
        "Page number": metadata.get("page", "N/A"),
        "Additional Metadata": metadata.get("section", "General Information")
    }


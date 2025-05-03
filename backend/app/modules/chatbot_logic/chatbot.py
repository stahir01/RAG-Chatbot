import os
from typing import List, Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain_core.retrievers import BaseRetriever
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.documents import Document
from backend.app.modules.document_retrieval import retrieve_text
from backend.app.config import (
    OPENAI_KEY,
    LANGSMITH_KEY,
    HUGGINGFACE_KEY,
    FALCON_MODEL,
    DEEPSEEK_MODEL,
    GPT_4o,
    VECTOR_DB_PATH,
    OPENAI_EMBED
)

DEFAULT_MODEL = GPT_4o

class CustomRetriever(BaseRetriever):
    """Wrapper for your existing retrieve_text function"""
    def __init__(self, vectordb_path: str, collection_name: str = "medical_dataset"):
        super().__init__()
        self.vectordb_path = vectordb_path
        self.collection_name = collection_name

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> List[Document]:
        results = retrieve_text(
            vectordb_path=self.vectordb_path,
            query=query,
            embed_model=OPENAI_EMBED,
            collection_name=self.collection_name,
            results_to_return=3
        )
        return [doc for doc, _ in results]


class Chatbot:
    def __init__(self, 
                model_type: str = 'openai',
                temperature: float = 0.2,
                max_tokens: int = 1024,
                vectordb_path: str = os.path.join(VECTOR_DB_PATH, "medical_dataset"),
                collection_name: str = "medical_dataset",
                top_p: float = 0.95):
        """
        Initializes the chatbot with Hugging Face API.

        Args:
            model_type (str): The type of model to use ('openai' or 'huggingface').
        """
        self.model_type = model_type
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.vectordb_path = vectordb_path
        self.collection_name = collection_name

        # Initialize components
        self.llm = self.initialize_model()
        self.retriever = CustomRetriever(self.vectordb_path, self.collection_name)
        self.qa_chain = self.create_qa_chain()
        self.chat_history = []

    def initialize_model(self):
        """Initialize the LLM with medical-focused parameters"""

        if self.model_type == 'openai':
            return ChatOpenAI(
                model=GPT_4o,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                api_key=OPENAI_KEY
            )
        else:
            return HuggingFaceEndpoint(
                    repo_id=DEEPSEEK_MODEL,
                    task="text-generation",
                    max_new_tokens=self.max_tokens,
                    do_sample=True,
                    top_k=3,
                    temperature=self.temperature,
                    huggingfacehub_api_token=HUGGINGFACE_KEY,
            )
        
    def create_qa_chain(self):
        
        contextualize_q_system_prompt = (
                "Given a chat history and latest user question about medical information,"
                "which might reference context in the chat history, "
                "formulate a standalone medical question "
                "that would be most effective for retrieving relevant information "
            )
        
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        # Create history-aware retriever
        history_aware_retriever = create_history_aware_retriever(
            self.llm,
            self.retriever,
            contextualize_q_prompt
        )

        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a medical assistant. Answer questions based on provided context 
            and chat history. Be precise and factual. If unsure, say you don't know.
            
            Context:
            {context}"""),
            MessagesPlaceholder("chat_history"),  
            ("human", "{input}"),
        ])

        document_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        return create_retrieval_chain(history_aware_retriever, document_chain)


    def generate_text(self, prompt: str) -> str:
        # Handle greetings
        if prompt.lower().strip() in ['hi', 'hello', 'hey']:
            return "Hello! I'm a medical AI assistant. How can I help you today?"
        
        # Run the QA chain
        response = self.qa_chain.invoke({
            "input": prompt,
            "chat_history": self.chat_history
        })
        
        # Update chat history
        self.chat_history.extend([
            HumanMessage(content=prompt),
            AIMessage(content=response["answer"])
        ])
        
        return response["answer"]

    def clear_history(self):
        self.chat_history = []


if __name__ == "__main__":
    # Test with explicit parameters
    chatbot = Chatbot(
        model_type='openai',
        temperature=0.3,
        max_tokens=1500,
        top_p=0.9
    )

    # First query
    response = chatbot.generate_text(
        "Persistent hip pain for 6 weeks with normal X-rays?"
    )
    print("First Response:", response)

    # Follow-up query
    response = chatbot.generate_text(
        "What diagnostic imaging would you recommend next?"
    )
    print("Follow-up Response:", response)

    # Clear history test
    chatbot.clear_history()
    print("History cleared. Current history length:", len(chatbot.chat_history))
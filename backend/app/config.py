import os
from configparser import ConfigParser
from dotenv import load_dotenv
from pathlib import Path

config = ConfigParser()

# Hugging Face API Key
HUGGINGFACE_KEY = os.getenv("HUGGINGFACE_KEY")

# OpenAI API Key
OPENAI_KEY = os.getenv("OPENAI_KEY")

# Hugging Face Model Names
DEEPSEEK_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"
FALCON_MODEL = "tiiuae/falcon-7b-instruct"

# Vector Database Configuration
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "vector_store")

#Embeddings
MINI_LM_EMBED = 'sentence-transformers/all-MiniLM-L6-v2'
OPENAI_EMBED = 'text-embedding-3-large'

#Documents Path
DOCUMENT_PATH  = os.getenv("DOCUMENT_PATH", "backend/app/documents")
PROJECT_ROOT = Path(__file__).parent


if __name__ == "__main__":
    print(f"Hugging Face API Key: {HUGGINGFACE_KEY}")
    print(f"OpenAI API Key: {OPENAI_KEY}")
    print(f"Root Directory: {PROJECT_ROOT}")

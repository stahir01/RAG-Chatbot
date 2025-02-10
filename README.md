## RAG System

### Introduction


This project implements a Retrieve-and-Generate (RAG) System using FastAPI, ChromaDB, and Hugging Face LLMs. The system retrieves relevant document passages and generates answers based on a given knowledge base.

The primary motivation behind this implementation is to create a self-contained knowledge retrieval system that does not rely on pre-trained knowledge within the LLM but rather dynamically retrieves context from provided documents.

A Jupyter Notebook is also provided for testing the individual components before running the full API. 


### Setting Up the Project

#### 1) Install Python and Create a Virtual Environment
First, make sure you have Python 3.9+ installed. Then, create a virtual environment:

```bash
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate on macOS/Linux
```
#### 2) Install Required Libraries
Once the virtual environment is activated, install dependencies:

```bash
pip install -r requirements.txt
```

#### 3) Create a .env File
The ```bash.env``` file is important in order to store HuggingFace credentials. Since this implementation uses Hugging Face models instead of OpenAI or Ollama, you need to add your API key:

```bash
HUGGINGFACE_Key = <your_huggingface_api_key>
```

#### 4) Run the FastAPI Server
To run the FastAPI server, execute the following command:

```bash
uvicorn main:app --reload
```

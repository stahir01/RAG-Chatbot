# Medical Analysis RAG Chatbot
This document outlines the setup and usage of a Retrieval-Augmented Generation (RAG) chatbot designed to answer medical questions in any language.

## Prerequisites

* Python 3.10+
* pip (Python package installer)
* Node.js and npm (Node Package Manager)
* API keys for Hugging Face and OpenAI

## Setup

### 1. Environment Variables

* Create a `.env` file in the **root directory** of the project with the following API keys:

    ```bash
    HUGGINGFACE_KEY=<YOUR_HUGGINGFACE_API_KEY>
    OPENAI_KEY=<YOUR_OPENAI_API_KEY>
    VECTOR_DB_PATH='backend/app/vector_store'
    ```
**Note:** Replace the placeholder values with your actual API keys obtained from the respective platforms.

### 2. Backend Setup

* Create and Activate Virtual Environment

    ```bash
    python3 -m venv Ragchatbot_Env # Create a virtual environment
    source Ragchatbot_Env/bin/activate  # Linux/macOS
    ```

* Install Dependencies

    ```bash
    pip install -r backend/requirements.txt
    ```

* 2.3. Create Embedding Database

    ```bash
    python3 -m backend.app.modules.document_retrieval.embedding_and_storage
    ```

* Run Backend Server: Navigate to the `backend` directory:

    ```bash
    cd backend
    ```

* Start the Uvicorn server:

    ```bash
    uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
    ```

This will start the backend server on localhost:8000, and you should see output indicating that the server is running.

### 3. Frontend Setup

* 3.1. Install Node.js Packages<br>
    Navigate to the `frontend` directory:

    ```bash
    cd frontend
    ```

* Install dependencies:

    ```bash
    npm install
    ```

* Run Frontend Server

    ```bash
    npm run start
    ```

This will typically open the frontend in your browser at `http://localhost:3000.`


* Ask medical questions in any language through the chatbot interface on http://localhost:3000. The chatbot will retrieve relevant information and generate an answer.

## Project Structure


## Explanation of Key Components


## Testing Using Jupyter Notebook

# AI Document Intelligence (RAG)

This project implements a Retrieval-Augmented Generation (RAG) system using Streamlit, LangChain, and Groq. It allows users to upload PDF documents and ask questions about their content.

## Features
- **PDF Upload**: Easily upload and process PDF documents.
- **Efficient Chunking**: Uses `RecursiveCharacterTextSplitter` for optimal context retrieval.
- **Fast Embeddings**: Leverages HuggingFace embeddings (`all-MiniLM-L6-v2`).
- **High-Performance Inference**: Powered by Groq's `llama-3.1-8b-instant`.
- **(New) Chat History**: Supports multi-turn conversations for interactive Q&A.
- **(New) Smart Retrieval**: Automatically adjusts retrieval depth for summary-type queries.

## Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ai-document-intelligence.git
    cd ai-document-intelligence
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables**:
    Create a `.env` file in the root directory and add your Groq API key:
    ```env
    GROQ_API_KEY=your_api_key_here
    ```

5.  **Run the application**:
    ```bash
    streamlit run app/app.py
    ```

## Project Structure
- `app/`: Contains the application logic.
- `data/`: Folder for sample documents.
- `faiss_index/`: Local storage for the FAISS vector database.
- `notebooks/`: Prototyping and exploration notebooks.

## Security Note
The `.env` file is excluded from version control via `.gitignore` to prevent API key leaks.

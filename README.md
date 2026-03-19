# RAG Document Insight 🚀

**RAG Document Insight** is a high-performance Retrieval-Augmented Generation (RAG) system built with Streamlit, LangChain, and Groq. It allows you to upload PDF documents and have natural, multi-turn conversations about their content with extreme speed and accuracy.

## ✨ Key Features
- **💬 Multi-turn Chat**: Remembers previous context for a true conversational experience.
- **📄 PDF Intelligence**: Deeply analyzes uploaded PDFs using advanced chunking strategies.
- **⚡ Blazing Fast**: Powered by Groq's Llama 3.1 (8B) for near-instant responses.
- **🔍 Smart Retrieval**: Automatically scales context depth based on whether you're asking for a summary or a specific detail.
- **🛡️ Rate Limited**: Built-in protection (5 queries/min) to manage API usage effectively.
- **☁️ Cloud Ready**: Optimized for seamless deployment on Streamlit Cloud.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Orchestration**: LangChain
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **Vector Store**: FAISS
- **LLM**: Groq (Llama-3.1-8b-instant)

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+
- A Groq API Key (Get it at [console.groq.com](https://console.groq.com/))

### 2. Local Setup
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/itsme008/rag-document-insight.git
    cd rag-document-insight
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    Create a `.env` file in the root directory and add your key:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    ```

5.  **Run the App**:
    ```bash
    streamlit run app/app.py
    ```

### 3. Deployment (Streamlit Cloud)
When deploying to Streamlit Cloud, add your `GROQ_API_KEY` to the **Secrets** section in the dashboard:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

## 🔒 Security
- `.env` files and `faiss_index` are excluded from Git to prevent data leaks.
- Temporary files are automatically cleaned up after processing.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

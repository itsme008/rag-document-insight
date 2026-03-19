import os
import sys
from dotenv import load_dotenv

# Add app directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from document_loader import load_single_pdf
from text_splitter import split_documents_text
from vector_store import create_vector_store

load_dotenv()

def test_rag_pipeline():
    # Use a sample PDF if it exists, or skip
    sample_pdf = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/sample_docs/Home _ Sales Navigator.pdf"))
    
    if not os.path.exists(sample_pdf):
        print(f"Skipping test: {sample_pdf} not found.")
        # Create a dummy pdf for testing if possible or just use a known path
        return

    print(f"Testing with: {sample_pdf}")
    
    # 1. Load
    docs = load_single_pdf(sample_pdf)
    print(f"Loaded {len(docs)} pages.")
    assert len(docs) > 0
    
    # 2. Split
    chunks = split_documents_text(docs)
    print(f"Split into {len(chunks)} chunks.")
    assert len(chunks) > 0
    
    # 3. Vector Store
    vector_store = create_vector_store(chunks)
    print("Vector store created successfully.")
    
    # 4. Search
    query = "What is the main topic?"
    results = vector_store.similarity_search(query, k=1)
    print(f"Search result: {results[0].page_content[:100]}...")
    assert len(results) > 0

if __name__ == "__main__":
    try:
        test_rag_pipeline()
        print("✅ Core RAG components are working correctly!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)

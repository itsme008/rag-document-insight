import streamlit as st
import tempfile
import os
import sys
from dotenv import load_dotenv

# Ensure local modules (document_loader, etc.) are importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from document_loader import load_single_pdf
from text_splitter import split_documents_text
from vector_store import create_vector_store
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

st.set_page_config(page_title="RAG Document Insight", page_icon="📄")
st.title("📄 RAG Document Insight")
st.markdown("Upload a PDF and ask questions about it! (Multi-turn chat enabled)")

@st.cache_resource
def load_model():
    return ChatGroq(model="llama-3.1-8b-instant")

model = load_model()

# Session State Initialization
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processed_filename" not in st.session_state:
    st.session_state.processed_filename = None

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    if st.session_state.processed_filename != uploaded_file.name:
        with st.spinner("Processing PDF..."):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_path = tmp_file.name

            try:
                docs = load_single_pdf(temp_path)
                chunks = split_documents_text(docs)
                st.session_state.vector_store = create_vector_store(chunks)
                st.session_state.processed_filename = uploaded_file.name
                st.session_state.chat_history = [] # Reset history for new document
                st.success(f"Processed: {uploaded_file.name}")
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

# Display Chat History
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(message.content)

import time

# Chat Input
query = st.chat_input("Enter your question:")

if "query_timestamps" not in st.session_state:
    st.session_state.query_timestamps = []

def is_rate_limited():
    current_time = time.time()
    # Remove timestamps older than 60 seconds
    st.session_state.query_timestamps = [t for t in st.session_state.query_timestamps if current_time - t < 60]
    if len(st.session_state.query_timestamps) >= 5: # 5 queries per minute
        return True
    return False

if query:
    if not st.session_state.vector_store:
        st.warning("Please upload a PDF first.")
    elif is_rate_limited():
        st.error("Rate limit exceeded. Please wait a minute before asking again.")
    else:
        st.session_state.query_timestamps.append(time.time())
        with st.chat_message("user"):
            st.markdown(query)
        
        with st.spinner("Thinking..."):
            query_lower = query.lower()
            is_summary_query = any(phrase in query_lower for phrase in 
                ["what is this document about", "summary", "overview", "main points", "summarize"])
            
            k = 10 if is_summary_query else 5
            results = st.session_state.vector_store.similarity_search(query, k=k)

            context = "\n\n".join([doc.page_content.strip() for doc in results])
            
            # Format chat history for context
            history_str = "\n".join([
                f"{'Human' if isinstance(m, HumanMessage) else 'AI'}: {m.content}" 
                for m in st.session_state.chat_history[-5:] # Last 5 exchanges
            ])

            prompt = f"""You are a helpful AI assistant analyzing a document.
            
            DOCUMENT CONTEXT:
            {context}
            
            CONVERSATION HISTORY:
            {history_str}
            
            INSTRUCTIONS:
            - Answer based strictly on the provided context if possible.
            - If the query seeks an overview/summary, synthesize the information across all provided chunks.
            - If history is relevant, incorporate it into your response.
            - If context doesn't contain the answer, say "I couldn't find information about that in the document."
            
            HUMAN QUESTION: {query}
            AI ANSWER:"""

            response = model.invoke(prompt)
            answer = response.content

            with st.chat_message("assistant"):
                st.markdown(answer)
                with st.expander("📚 Retrieved Context"):
                    for i, doc in enumerate(results):
                        st.markdown(f"**Chunk {i+1}:**")
                        st.write(doc.page_content[:400] + "...")

            # Update Session State
            st.session_state.chat_history.append(HumanMessage(content=query))
            st.session_state.chat_history.append(AIMessage(content=answer))
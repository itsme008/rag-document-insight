from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def load_vector_store(path="faiss_index"):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vector_store = FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store


def retrieve_documents(vector_store, query, k=3):
    return vector_store.similarity_search(query, k=k)

if __name__ == "__main__":
    vector_store = load_vector_store()

    query = input("Enter your query: ")

    results = retrieve_documents(vector_store, query)

    for i, doc in enumerate(results):
        print(f"Result {i + 1}:")
        print(doc.page_content[:200])
        print("-" * 50)
from langchain_text_splitters import RecursiveCharacterTextSplitter
def split_documents_text(docs, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return text_splitter.split_documents(docs)


if __name__ == "__main__":
    from document_loader import load_documents
    docs = load_documents("data/sample_docs")
    chunks = split_documents_text(docs)

    print("Number of chunks:", len(chunks))
    print(chunks[0].page_content[:200])
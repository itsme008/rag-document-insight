from langchain_community.document_loaders import PyPDFLoader
import os


def load_documents(folder_path):
    if not os.path.exists(folder_path):
        raise ValueError(f"Folder not found: {folder_path}")

    documents = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(folder_path, file)

            loader = PyPDFLoader(file_path)
            docs = loader.load()

            documents.extend(docs)

    return documents


def load_single_pdf(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()


if __name__ == "__main__":
    docs = load_documents("data/sample_docs")

    print("Pages loaded:", len(docs))
    print(docs[0].page_content[:200])
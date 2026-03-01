from rag.chunker import chunk_text
from rag.retriever import VectorStore
from rag.loader import load_documents_from_folder

vector_store = VectorStore()

def ingest_text(text):
    chunks = chunk_text(text)
    vector_store.add_documents(chunks)
    return len(chunks)
def ingest_folder(folder_path="documents"):
    text = load_documents_from_folder(folder_path)

    if not text:
        return 0

    chunks = chunk_text(text)
    vector_store.add_documents(chunks)

    return len(chunks)
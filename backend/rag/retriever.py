import faiss
import numpy as np
from rag.embedder import get_embedding

class VectorStore:
    def __init__(self, dim=768):
        self.index = faiss.IndexFlatL2(dim)
        self.text_chunks = []

    def add_documents(self, chunks):
        embeddings = [get_embedding(chunk) for chunk in chunks]
        self.index.add(np.array(embeddings))
        self.text_chunks.extend(chunks)

    # def search(self, query, top_k=3):
    #     query_embedding = np.array([get_embedding(query)])
    #     distances, indices = self.index.search(query_embedding, top_k)
    #     return [self.text_chunks[i] for i in indices[0]]
    def search(self, query, top_k=3):
        query_embedding = np.array([get_embedding(query)])
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                "text": self.text_chunks[idx],
                "score": float(distances[0][i])
            })

        return results
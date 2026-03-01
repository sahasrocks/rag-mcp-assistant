import requests
import numpy as np

EMBED_URL = "http://localhost:11434/api/embeddings"

def get_embedding(text, model="nomic-embed-text"):
    response = requests.post(
        EMBED_URL,
        json={
            "model": model,
            "prompt": text
        }
    )

    embedding = response.json()["embedding"]
    return np.array(embedding).astype("float32")
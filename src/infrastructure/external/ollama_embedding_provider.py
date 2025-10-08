import requests


class OllamaEmbeddingProvider:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "nomic-embed-text"):
        self.base_url = base_url
        self.model = model

    def get_embedding(self, text: str) -> list[float]:
        response = requests.post(f"{self.base_url}/api/embeddings", json={"model": self.model, "prompt": text})
        response.raise_for_status()
        return response.json()["embedding"]

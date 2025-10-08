import pickle
from pathlib import Path


class FileEmbeddingRepository:
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._embeddings: dict[str, list[float]] = {}
        self._load()

    def is_exists(self) -> bool:
        return len(self._embeddings) > 0

    def _load(self) -> None:
        if self._file_path.exists():
            with open(self._file_path, "rb") as f:
                self._embeddings = pickle.load(f)

    def save_embedding(self, series_id: str, embedding: list[float]) -> None:
        self._embeddings[series_id] = embedding

    def get_embedding(self, series_id: str) -> list[float] | None:
        return self._embeddings.get(series_id)

    def get_all_embeddings(self) -> dict[str, list[float]]:
        return self._embeddings.copy()

    def save(self) -> None:
        with open(self._file_path, "wb") as _file:
            pickle.dump(self._embeddings, _file)

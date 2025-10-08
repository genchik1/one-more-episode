import pickle
from pathlib import Path


class FileEmbeddingRepository:
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._embeddings: dict[int, list[float]] = {}
        self._load()

    def _load(self) -> None:
        if self._file_path.exists():
            with open(self._file_path, "rb") as f:
                self._embeddings = pickle.load(f)
            self.is_exists = True
        else:
            self.is_exists = False

    def add_embedding(self, series_id: int, embedding: list[float]) -> None:
        self._embeddings[series_id] = embedding

    def get_embedding(self, series_id: int) -> list[float] | None:
        return self._embeddings.get(series_id)

    def get_all_embeddings(self) -> dict[int, list[float]]:
        return self._embeddings

    def save_embeddings(self) -> None:
        with open(self._file_path, "wb") as _file:
            pickle.dump(self._embeddings, _file)

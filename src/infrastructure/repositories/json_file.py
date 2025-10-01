import json
from typing import Any


class JsonFileRepository:
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def read(self) -> dict[Any, Any] | None:
        try:
            with open(self._file_path, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return None

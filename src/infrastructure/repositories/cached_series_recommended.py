import pickle
from typing import Generator

import redis

from src.domain import repositories
from src.domain.models import ItemFeatures


class SimpleSeriesRecommendedService:
    def __init__(self, ollama_url: str, model: str):
        self._ollama_url = ollama_url
        self._model = model

    def create_series_text(self, series):
        """Создаем полный текстовый контекст для сериала"""
        parts = [f"Название: {series['title']}", f"Описание: {series['description']}"]

        if "genres" in series and series["genres"]:
            parts.append(f"Жанры: {', '.join(series['genres'])}")

        if "actors" in series and series["actors"]:
            parts.append(f"Актеры: {', '.join(series['actors'])}")

        if "year" in series:
            parts.append(f"Год: {series['year']}")

        if "rating" in series:
            parts.append(f"Рейтинг: {series['rating']}")

        return ". ".join(parts)

    def get_embedding(self, text):
        """Получение эмбеддинга через Ollama"""
        response = requests.post(f"{self._ollama_url}/api/embeddings", json={"model": self._model, "prompt": text})
        return response.json()["embedding"]

    def add_series(self, series_list):
        """Добавление сериалов и создание эмбеддингов"""
        self._series_data = series_list

        for series in self._series_data:
            # Создаем полный текст для сериала
            series_text = self.create_series_text(series)

            # Генерируем эмбеддинг
            embedding = self.get_embedding(series_text)
            self._embeddings.append(embedding)

            # Сохраняем текст для отладки
            series["_embedding_text"] = series_text

        self._embeddings = np.array(self._embeddings)

    def search(self, query, top_k=5):
        """Поиск по любому текстовому запросу"""
        query_embedding = self.get_embedding(query)
        query_embedding = np.array(query_embedding).reshape(1, -1)

        similarities = cosine_similarity(query_embedding, self._embeddings)[0]

        results = []
        for idx in np.argsort(similarities)[::-1][:top_k]:
            results.append(
                {
                    "series": self._series_data[idx],
                    "similarity": similarities[idx],
                    "embedding_text": self._series_data[idx].get("_embedding_text", ""),
                }
            )

        return results


class CachedSeriesRecommenderRepository:
    def __init__(self, cache_repository: repositories.IDbRepository) -> None:
        self._cache_file = cache_file_name
        self._series_data = []
        self._embeddings = []
        self._cache_repository = cache_repository
        self._item_fields = [
            "id",
            "genres",
            "name",
            "persons",
            "short_description",
            "description",
            "slogan",
            "en_name",
        ]

    async def add_series(self, series_list):
        self._series_data = series_list

        async for batch_item_keys in self._cache_repository.get_all_item_keys():
            items = await self._cache_repository.get_item_features(batch_item_keys, features=self._item_fields)

            for item in items:
                item_dict = item.model_dump(exclude_defaults=True, exclude_none=True)
                item_text = ", ".join([f"{key}: {value}" for key, value in item_dict.items()])

            # Генерируем эмбеддинг
            embedding = self.get_embedding(series_text)
            self._embeddings.append(embedding)

            # Сохраняем текст для отладки
            series["_embedding_text"] = series_text

        self._embeddings = np.array(self._embeddings)

    def save_embeddings(self):
        cache_data = {"series_data": self.series_data, "embeddings": self.embeddings}
        with open(self._cache_file, "wb") as f:
            pickle.dump(cache_data, f)

    def load_embeddings(self):
        """Загрузка эмбеддингов из файла"""
        if Path(self._cache_file).exists():
            with open(self._cache_file, "rb") as f:
                cache_data = pickle.load(f)
                self.series_data = cache_data["series_data"]
                self.embeddings = cache_data["embeddings"]
            return True
        return False

    def add_series(self, series_list, use_cache=True):
        """Добавление сериалов с использованием кэша"""
        if use_cache and self.load_embeddings():
            print("✅ Эмбеддинги загружены из кэша")
            return

        print("🔄 Генерация новых эмбеддингов...")
        super().add_series(series_list)
        self.save_embeddings()
        print("✅ Эмбеддинги сохранены в кэш")

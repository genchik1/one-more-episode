from dataclasses import dataclass
from typing import Final
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from src.infrastructure import repositories, external

@dataclass
class Recommendation:
    series_id: int
    similarity_score: float
    reason: str

class SeriesRecommendationService:
    ITEM_FEATURES: Final[list[str]] = [
        "id",
        "genres",
        "name",
        "persons",
        "short_description",
        "description",
        "slogan",
        "en_name",
    ]

    def __init__(
        self,
        series_repository: repositories.RedisRepository,
        file_embedding: repositories.FileEmbeddingRepository,
        embedding_provider: external.OllamaEmbeddingProvider,
    ) -> None:
        self._series_repository = series_repository
        self._file_embedding = file_embedding
        self._embedding_provider = embedding_provider
        self._series_list = []
        self.is_load: bool = False

    async def load(self, force_refresh: bool = False) -> None:
        """Load data and prepare embeddings"""
        if self.is_load:
            return
        await self._load_series()
        self._series_ids = [series.id for series in self._series_list]

        if not force_refresh or not self._file_embedding.is_exists():
            self._load_cached_embeddings()

        # # Generate missing embeddings
        # self._generate_missing_embeddings()
        #
        # # Prepare embedding matrix for efficient similarity calculation
        self._prepare_embedding_matrix()

        # self._file_embedding.save()
        self.is_load = True

    async def _load_series(self) -> None:
        series = []
        async for batch_ids in self._series_repository.get_all_item_ids():
            items = await self._series_repository.get_item_features(batch_ids, self.ITEM_FEATURES)
            series.extend(items)
        self._series_list = series

    def _load_cached_embeddings(self) -> None:
        """Load embeddings from repository"""
        self._series_embeddings = self._file_embedding.get_all_embeddings()

    def _generate_missing_embeddings(self) -> None:
        """Generate embeddings for series without cached ones"""
        for series in self._series_list:
            if series.id not in self._series_embeddings:
                series_dict = series.model_dump(exclude_defaults=True, exclude_none=True)
                context = ", ".join([f"{key}: {value}" for key, value in series_dict.items()])
                embedding = self._embedding_provider.get_embedding(context)
                self._series_embeddings[series.id] = embedding
                self._file_embedding.save_embedding(series.id, embedding)

    def _prepare_embedding_matrix(self) -> None:
        embeddings_list = []
        valid_series_ids = []

        # for series_id in self._series_ids:
        #     if series_id in self._series_embeddings:
        #         embeddings_list.append(self._series_embeddings[series_id])
        #         valid_series_ids.append(series_id)

        for series_id, embedding in self._series_embeddings.items():
            embeddings_list.append(embedding)
            valid_series_ids.append(series_id)

        self._embedding_matrix = np.array(embeddings_list)
        self._series_ids = valid_series_ids

    def predict(self, query: str, top_k: int = 5) -> list[Recommendation]:
        """Generate recommendations based on query"""
        # # Check cache first
        # cache_key = f"query:{query}:top_k:{top_k}"
        # cached = self.cache_provider.get(cache_key)
        # if cached:
        #     return cached

        # Generate query embedding
        query_embedding = self._embedding_provider.get_embedding(query)
        query_embedding = np.array(query_embedding).reshape(1, -1)

        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self._embedding_matrix)[0]

        # Get top recommendations
        recommendations = self._build_recommendations(similarities, top_k, query)

        # Cache results
        # self.cache_provider.set(cache_key, recommendations, ttl=3600)  # 1 hour

        return recommendations

    # def find_similar(self, series_id: str, top_k: int = 5) -> List[Recommendation]:
    #     """Find similar series based on content"""
    #     if series_id not in self._series_embeddings:
    #         raise ValueError(f"Series with id {series_id} not found")
    #
    #     # Get target series index
    #     target_idx = self._series_ids.index(series_id)
    #     target_embedding = self._embedding_matrix[target_idx].reshape(1, -1)
    #
    #     # Calculate similarities (excluding the target series)
    #     similarities = cosine_similarity(target_embedding, self._embedding_matrix)[0]
    #     similarities[target_idx] = -1  # Exclude self
    #
    #     return self._build_recommendations(similarities, top_k, f"similar to {series_id}")

    def _build_recommendations(self, similarities: np.ndarray, top_k: int, context: str) -> list[Recommendation]:
        """Build recommendation objects from similarity scores"""
        top_indices = np.argsort(similarities)[::-1][:top_k]

        recommendations = []
        for idx in top_indices:
            if similarities[idx] > 0:  # Only include positive similarities
                series_id = self._series_ids[idx]
                recommendations.append(Recommendation(
                    series_id=series_id,
                    similarity_score=float(similarities[idx]),
                    reason=f"Based on your query: {context}"
                ))

        return recommendations

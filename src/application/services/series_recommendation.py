import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from src.application.commands import SimilarityItemCommand
from src.application.services.embeddings_factory import EmbeddingsFactoryService
from src.infrastructure import external


class SeriesRecommendationService:
    def __init__(
        self,
        embeddings_factory_service: EmbeddingsFactoryService,
        embedding_provider: external.OllamaEmbeddingProvider,
    ) -> None:
        self._embeddings_factory_service = embeddings_factory_service
        self._embedding_provider = embedding_provider
        self._embedding_matrix: list[float] = []
        self._series_ids: list[int] = []

    def load(self) -> None:
        embeddings = self._embeddings_factory_service.get()
        self._prepare_embedding_matrix(embeddings)

    def _prepare_embedding_matrix(self, embeddings: dict[int, list[float]]) -> None:
        embeddings_list = []
        valid_series_ids = []

        for series_id, embedding in embeddings.items():
            embeddings_list.append(embedding)
            valid_series_ids.append(series_id)

        self._embedding_matrix = np.array(embeddings_list)
        self._series_ids = valid_series_ids

    def predict(self, query: str, count: int = 5) -> list[SimilarityItemCommand]:
        query_embedding = self._embedding_provider.get_embedding(query)
        query_embedding = np.array(query_embedding).reshape(1, -1)

        similarities = cosine_similarity(query_embedding, self._embedding_matrix)[0]
        return self._build_recommendations(similarities, count)

    def _build_recommendations(self, similarities: np.ndarray, count: int) -> list[SimilarityItemCommand]:
        recommendations = []
        for idx in np.argsort(similarities)[::-1][:count]:
            if similarities[idx] > 0:
                series_id = self._series_ids[idx]
                recommendations.append(
                    SimilarityItemCommand(
                        id=series_id,
                        score=float(similarities[idx]),
                    )
                )

        return recommendations

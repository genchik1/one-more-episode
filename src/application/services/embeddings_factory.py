from typing import Final

from src.application.errors import DoesNotExistsDataError
from src.domain.logger import ILogger
from src.domain.models import ItemFeatures
from src.infrastructure import external, repositories


class EmbeddingsFactoryService:
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
    TEMPLATE: str = """
        Название: {name}
        Оригинальное название: {en_name}
        Жанры: {genres}
        Страна: {country}
        Описание: {description}
        Актеры: {persons}
        Ключевые слова: {short_description}
    """

    def __init__(
        self,
        logger: ILogger,
        series_repository: repositories.RedisRepository,
        file_embedding: repositories.FileEmbeddingRepository,
        embedding_provider: external.OllamaEmbeddingProvider,
    ) -> None:
        self._logger = logger
        self._series_repository = series_repository
        self._file_embedding = file_embedding
        self._embedding_provider = embedding_provider
        self._series_embeddings: dict[int, list[float]] = {}

    def get(self) -> dict[int, list[float]]:
        if not self._series_embeddings:
            self._logger.info("Not exists embeddings")
            raise DoesNotExistsDataError("Not exists embeddings")
        return self._series_embeddings

    async def load(self) -> None:
        self._logger.info("Start load embeddings")
        if self._file_embedding.is_exists:
            self._logger.info("File with embeddings exists")
            self._series_embeddings = self._file_embedding.get_all_embeddings()
        else:
            self._logger.info("File with embeddings not exists, start create")
            await self._load_series()
            self._generate_missing_embeddings()
            self._file_embedding.save_embeddings()

    async def _load_series(self) -> None:
        series = []
        step = 1
        async for batch_ids in self._series_repository.get_all_item_ids():
            self._logger.info("load series batch", extra={"step": step})
            items = await self._series_repository.get_item_features(batch_ids, self.ITEM_FEATURES)
            series.extend(items)
            step += 1
        self._series_list = series

    def _get_item_context(self, item: ItemFeatures) -> str:
        dict_for_template = {
            "name": item.name or "",
            "description": item.description or "",
            "genres": ", ".join(genre.name for genre in (item.genres or [])),
            "country": ", ".join(country.name for country in (item.countries or [])),
            "persons": ", ".join(person.name for person in (item.persons or [])),
            "short_description": item.short_description or "",
            "en_name": item.en_name or item.name or "",
        }
        return self.TEMPLATE.format(**dict_for_template)

    def _generate_missing_embeddings(self) -> None:
        count_series = list(self._series_list)
        self._logger.info("start generate_missing_embeddings", extra={"count_series": count_series})
        for step, series in enumerate(self._series_list, 1):
            if series.id in self._series_embeddings:
                continue
            context = self._get_item_context(series)
            embedding = self._embedding_provider.get_embedding(context)
            self._series_embeddings[series.id] = embedding
            self._file_embedding.add_embedding(series.id, embedding)
            if step % 100 == 0:
                self._logger.info("generate_missing_embeddings", extra={"step": f"{step}/{count_series}"})
        self._logger.info("done generate_missing_embeddings")

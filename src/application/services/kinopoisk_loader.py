from collections.abc import Callable

from src.consts import COLLECTIONS
from src.domain import pipeline, repositories
from src.domain.logger import ILogger
from src.domain.models import ItemFeatures, ItemsCollection
from src.settings import KinopoiskConfig


class KinopoiskDataLoaderService:
    """Сервис для загрузки данных из Кинопоиска в базы данных"""

    def __init__(
        self,
        config: KinopoiskConfig(),
        logger: ILogger,
        kinopoisk_repository: repositories.IKinopoiskRepository,
        cache_repository: repositories.IDbRepository,
        file_repository: repositories.IFileRepository,
        callable_pipeline_func: Callable[[list[ItemFeatures]], pipeline.IPipelineBuilder],
    ) -> None:
        self._logger = logger
        self._kinopoisk_repo = kinopoisk_repository
        self._cache_repository = cache_repository
        self._file_repository = file_repository
        self._config = config
        self._callable_pipeline_func = callable_pipeline_func

    def get_actual_page_number(self) -> int:
        return self._file_repository.read()

    def save_actual_page_number(self, page: int) -> None:
        self._file_repository.write(page)

    async def save_item_features(self, collection: list[ItemFeatures]) -> None:
        await self._cache_repository.save_item_features(collection)

    async def save_collection(self, collection: ItemsCollection) -> None:
        await self._cache_repository.save_collection(collection)

    async def load_series_info(self) -> None:
        self._logger.info("Start load series info from kp")
        while True:
            page = self.get_actual_page_number()
            self._logger.info(f"page: {page} >>")
            media_item_list = await self._kinopoisk_repo.load_series(
                self._config.base_url,
                {
                    "limit": self._config.limit,
                    "page": page,
                    "sortField": "id",
                    "sortType": "1",
                    "type": "tv-series",
                },
                self._config.x_api_key,
            )
            collection = ItemsCollection(items=media_item_list)
            filtered_media_item_list = await self._callable_pipeline_func(collection=collection).execute()
            await self.save_item_features(filtered_media_item_list.items)
            if len(media_item_list) < self._config.limit:
                break
            page += 1
            self.save_actual_page_number(page)

    async def load_collection(self, collection_slug: str) -> None:
        page = 1
        collection_items_ids: list[ItemFeatures] = []
        while True:
            media_item_list = await self._kinopoisk_repo.load_series(
                self._config.base_url,
                {
                    "limit": self._config.limit,
                    "selectFields": "id",
                    "lists": collection_slug,
                    "page": page,
                },
                self._config.x_api_key,
            )
            collection_items_ids.extend(media_item_list)
            if len(media_item_list) < self._config.limit:
                break

        collection = ItemsCollection(
            slug=collection_slug,
            name=COLLECTIONS[collection_slug]["name"],
            items=collection_items_ids,
        )
        await self.save_collection(collection)

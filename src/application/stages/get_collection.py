from src.application.stages.errors import StageError
from src.domain import repositories
from src.domain.models import ItemsCollection
from src.domain.pipeline import IPipelineStage
from src.infrastructure.repositories.errors import ReadError


class GetCollectionStage(IPipelineStage):
    def __init__(self, cache_repository: repositories.IDbRepository, collection_slug: str, features: list[str]) -> None:
        self._cache_repository = cache_repository
        self._collection_slug = collection_slug
        self._features = features

    async def process(self, collection: ItemsCollection | None = None) -> ItemsCollection:
        if collection.items:
            return collection
        try:
            collection = await self._cache_repository.get_collection(self._collection_slug)
        except ReadError as err:
            raise StageError from err
        item_ids = [item.id for item in collection.items]
        collection.items = await self._cache_repository.get_item_features(item_ids, self._features)
        return collection

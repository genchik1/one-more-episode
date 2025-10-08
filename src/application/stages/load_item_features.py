from src.domain import repositories
from src.domain.models import ItemsCollection
from src.domain.pipeline import IPipelineStage


class LoadItemFeaturesStage(IPipelineStage):
    def __init__(
        self,
        cache_repository: repositories.IDbRepository,
        features: list[str],
    ) -> None:
        self._cache_repository = cache_repository
        self._features = features

    async def process(self, collection: ItemsCollection | None = None) -> ItemsCollection:
        all_items_ids = [item.id for item in collection.items]
        collection.items = await self._cache_repository.get_item_features(all_items_ids, self._features)
        return collection

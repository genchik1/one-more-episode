from src.application.stages.errors import StageError
from src.domain import repositories
from src.domain.models import ItemsCollection
from src.domain.pipeline import IPipelineStage


class GetOnboardingCollectionV1Stage(IPipelineStage):
    def __init__(
        self,
        cache_repository: repositories.IDbRepository,
        file_repository: repositories.IFileRepository,
        features: list[str],
        name: str,
        slug: str | None = None,
    ) -> None:
        self._cache_repository = cache_repository
        self._file_repository = file_repository
        self._features = features
        self.collection = ItemsCollection(name=name, slug=slug)

    async def process(self, collection: ItemsCollection | None = None) -> ItemsCollection:
        if collection.items:
            return collection
        redactor_collections = self._file_repository.read()
        if not redactor_collections:
            raise StageError("not found")
        all_items_ids = [item["id"] for collection in redactor_collections for item in collection["items"]]
        self.collection.items = await self._cache_repository.get_item_features(all_items_ids, self._features)
        return self.collection

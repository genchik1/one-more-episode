from src.domain.models import ItemsCollection
from src.domain.pipeline import IPipelineStage


class AddCollectionStage(IPipelineStage):
    def __init__(self, collection: ItemsCollection) -> None:
        self._collection = collection

    async def process(self, collection: ItemsCollection | None = None) -> ItemsCollection:
        return self._collection

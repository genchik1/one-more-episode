from src.domain.models import ItemsCollection
from src.domain.pipeline import IPipelineStage


class FilterWithoutPreviewUrlStage(IPipelineStage):
    async def process(self, collection: ItemsCollection) -> ItemsCollection:
        collection.items = [title for title in collection.items if title.poster and title.poster.preview_url]
        return collection

from src.domain.models import ItemsCollection
from src.domain.pipeline import IPipelineStage


class FilterByRatingStage(IPipelineStage):
    def __init__(self, min_rating: float) -> None:
        self._min_rating = min_rating

    async def process(self, collection: ItemsCollection) -> ItemsCollection:
        collection.items = [
            title for title in collection.items if title.rating and title.rating.get("kp", 0) > self._min_rating
        ]
        return collection

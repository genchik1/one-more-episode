from src.application import stages
from src.domain.models import ItemFeatures, ItemsCollection
from src.domain.repositories import IDbRepository


class TestCacheRepository(IDbRepository):
    def __init__(self, media_items: list[ItemFeatures]) -> None:
        self._items = media_items

    async def get_collection(self, collection_name: str) -> ItemsCollection:
        return ItemsCollection(items=self._items)

    async def get_item_features(self, identifiers: list[int], features: list[str]) -> list[ItemFeatures]:
        return self._items[:3]


async def test_get_collection(item_features: list[ItemFeatures]) -> None:
    mock_repository = TestCacheRepository(item_features)
    features = ["rating"]
    stage = stages.GetCollectionStage(mock_repository, "test", features)
    filtered_collections = await stage.process()
    assert len(filtered_collections) == 3
    assert filtered_collections[0].id == 1

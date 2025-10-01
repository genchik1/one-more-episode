import pytest

from src.application.stages import FilterByRatingStage
from src.domain.models import ItemFeatures, ItemsCollection


@pytest.fixture
def items() -> list[ItemFeatures]:
    collection = [
        ItemFeatures(
            id=1,
            rating={
                "filmCritics": 0,
                "imdb": 7.5,
                "kp": 8.109,
            },
        ),
        ItemFeatures(
            id=2,
            rating={
                "await": None,
                "russianFilmCritics": 0,
            },
        ),
        ItemFeatures(
            id=3,
            rating={
                "kp": 4,
                "russianFilmCritics": 0,
            },
        ),
        ItemFeatures(
            id=4,
        ),
    ]
    return collection


async def test_filter_by_rating(items: list[ItemFeatures]) -> None:
    stage = FilterByRatingStage(min_rating=4)
    collection = ItemsCollection(items=items)
    filtered_collection = await stage.process(collection)
    assert len(filtered_collection.items) == 1
    assert filtered_collection.items[0].id == 1

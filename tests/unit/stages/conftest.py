import pytest

from src.domain.models import ItemFeatures


@pytest.fixture
def item_features() -> list[ItemFeatures]:
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

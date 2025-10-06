import json
import os

import pytest

from src import settings
from src.application.dtos import KpMediaItem
from src.domain.models import ItemFeatures
from src.infrastructure.external.clients import init_redis_media_items
from src.infrastructure.repositories import RedisRepository
from src.settings import RedisConfig
from tests.utils import TestLogger


@pytest.fixture
def kp_item() -> str:
    return json.dumps(
        {
            "countries": [{"name": "Россия"}],
            "externalId": {"kpHD": "4614d5da06a58aada1cb5122974002c4", "tmdb": 6395},
            "genres": [
                {"name": "триллер"},
                {"name": "драма"},
                {"name": "мелодрама"},
                {"name": "детектив"},
            ],
            "id": 79429,
            "name": "Мастер и Маргарита",
            "persons": [
                {
                    "description": "Маргарита",
                    "enName": None,
                    "enProfession": "actor",
                    "id": 251229,
                    "name": "Анна Ковальчук",
                    "photo": "https://image.openmoviedb.com/kinopoisk-st-images//actor_iphone/iphone360_251229.jpg",
                    "profession": "актеры",
                },
                {
                    "description": "Мастер",
                    "enName": None,
                    "enProfession": "actor",
                    "id": 294521,
                    "name": "Александр Галибин",
                    "photo": "https://image.openmoviedb.com/kinopoisk-st-images//actor_iphone/iphone360_294521.jpg",
                    "profession": "актеры",
                },
            ],
            "poster": {
                "previewUrl": "https://image.openmoviedb.com/kinopoisk-images/1777765/f4a048de-ccca-4ed0-a789-5c848c738f2e/300x450",
                "url": "https://image.openmoviedb.com/kinopoisk-images/1777765/f4a048de-ccca-4ed0-a789-5c848c738f2e/600x900",
            },
            "rating": {
                "await": None,
                "filmCritics": 0,
                "imdb": 7.5,
                "kp": 8.109,
                "russianFilmCritics": 0,
            },
            "releaseYears": [{"end": 2005, "start": 2005}],
            "seasonsInfo": [{"episodesCount": 10, "number": 1}],
            "seriesLength": 50,
            "shortDescription": "Нечистая сила в Москве середины 1930-х. "
            "Режиссер «Собачьего сердца» бережно экранизирует роман Булгакова",
            "status": "completed",
            "totalSeriesLength": 500,
            "updatedAt": "2025-09-16T16:55:33.423Z",
            "year": 2005,
        }
    )


@pytest.fixture
def media_item(kp_item: str) -> KpMediaItem:
    return KpMediaItem.model_validate_json(kp_item)


@pytest.fixture
def item_features(media_item: KpMediaItem) -> ItemFeatures:
    return ItemFeatures(**media_item.model_dump(exclude_defaults=True, exclude_none=True, by_alias=False))


@pytest.fixture(scope="session")
def logger() -> TestLogger:
    return TestLogger("test")


@pytest.fixture(scope="session")
def redis_config() -> RedisConfig:
    return settings.REDIS


@pytest.fixture(scope="session")
def redis_client(redis_config: RedisConfig, logger: TestLogger):
    os.environ["REDIS_DB"] = "15"
    yield init_redis_media_items(redis_config, logger)


@pytest.fixture
async def cache_repository(redis_client):
    for key in await redis_client.keys():
        await redis_client.delete(key)
    yield RedisRepository(redis_client)

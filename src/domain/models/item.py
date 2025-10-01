from datetime import datetime
from functools import lru_cache
from typing import Any

from pydantic import BaseModel, Field

from src.consts import MediaType


class Country(BaseModel):
    name: str


class Genre(BaseModel):
    name: str


class Person(BaseModel):
    person_id: int
    name: str = Field(default="")
    photo: str
    profession: str


class Poster(BaseModel):
    preview_url: str | None = Field(default=None)
    url: str | None = Field(default=None)


class ReleaseYear(BaseModel):
    start: int | None = Field(default=None)
    end: int | None = Field(default=None)


class SeasonsInfo(BaseModel):
    episodes_count: int
    number: int


class SequelPrequel(BaseModel):
    id: int
    name: str | None = Field(default=None)
    type: MediaType


class Rating(BaseModel):
    r_await: float | None = Field(default=None)
    filmCritics: float | None = Field(default=None)
    imdb: float | None = Field(default=None)
    kp: float | None = Field(default=None)
    russianFilmCritics: float | None = Field(default=None)


class SimilarMovie(BaseModel):
    id: int
    type: MediaType
    alternativeName: str | None = Field(default=None)
    name: str
    poster: Poster


class ItemFeatures(BaseModel):
    id: int
    countries: list[Country] = Field(default=[])
    external_id: dict[str, str | Any] = Field(default={})
    genres: list[Genre] = Field(default=[])
    name: str = Field(default="")
    persons: list[Person] = Field(default=[])
    poster: Poster | None = Field(default=None)
    rating: dict[str, float | None] = Field(default={})
    release_years: list[ReleaseYear] = Field(default=[])
    seasons_info: list[SeasonsInfo] = Field(default=[])
    sequels_and_prequels: list[SequelPrequel] = Field(default=[])
    series_length: int = Field(default=0)
    short_description: str = Field(default="")
    similar_movies: list[SimilarMovie] = Field(default=[])
    status: str = Field(default="")
    total_series_length: int = Field(default=0)
    year: int = Field(default=0)
    kp_updated_at: datetime | None = Field(default=None)
    description: str = Field(default="")
    slogan: str = Field(default="")
    en_name: str = Field(default="")

    @classmethod
    @lru_cache
    def get_numerated_keys(cls) -> dict[str, int]:
        return {
            "id": 1,
            "countries": 2,
            "external_id": 3,
            "genres": 4,
            "name": 5,
            "persons": 6,
            "poster": 7,
            "rating": 8,
            "release_years": 9,
            "seasons_info": 10,
            "sequels_and_prequels": 11,
            "series_length": 12,
            "short_description": 13,
            "similar_movies": 14,
            "status": 15,
            "total_series_length": 16,
            "year": 17,
            "kp_updated_at": 18,
            "description": 19,
            "slogan": 20,
            "en_name": 21,
        }

    @classmethod
    def replace_key(cls, key: str) -> str:
        return str(cls.get_numerated_keys()[key])

    @classmethod
    def get_real_key(cls, key: str) -> str:
        for real_key, num_key in cls.get_numerated_keys().items():
            if str(num_key) == key:
                return real_key


class ItemsCollection(BaseModel):
    name: str = Field(default="")
    slug: str = Field(default="")
    items: list[ItemFeatures] = Field(default=[])

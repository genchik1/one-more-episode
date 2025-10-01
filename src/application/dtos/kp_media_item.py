from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from src.consts import MediaType


class Country(BaseModel):
    name: str


class Genre(BaseModel):
    name: str


class Person(BaseModel):
    person_id: int = Field(alias="id")
    name: str | None
    photo: str
    profession: str


class Poster(BaseModel):
    preview_url: str | None = Field(alias="previewUrl")
    url: str | None


class ReleaseYear(BaseModel):
    start: int | None
    end: int | None


class SeasonsInfo(BaseModel):
    episodes_count: int = Field(alias="episodesCount")
    number: int


class SequelPrequel(BaseModel):
    id: int = Field(alias="id")
    name: str | None
    type: MediaType


class Rating(BaseModel):
    r_await: float | None = Field(alias="await")
    filmCritics: float | None
    imdb: float | None
    kp: float | None
    russianFilmCritics: float | None


class SimilarMovie(BaseModel):
    id: int = Field(alias="id")
    type: MediaType
    alternativeName: str | None
    name: str
    poster: Poster


class KpMediaItem(BaseModel):
    id: int = Field(alias="id")
    countries: list[Country] = Field(default=None)
    external_id: dict[str, str | Any] = Field(default=None, alias="externalId")
    genres: list[Genre] = Field(default=None)
    name: str | None = Field(default=None)
    persons: list[Person] = Field(default=None)
    poster: Poster | None = Field(default=None)
    rating: dict[str, float | None] = Field(default=None)
    release_years: list[ReleaseYear] = Field(default=None, alias="releaseYears")
    seasons_info: list[SeasonsInfo] | None = Field(default=None, alias="seasonsInfo")
    sequels_and_prequels: list[SequelPrequel] | None = Field(default=None, alias="sequelsAndPrequels")
    series_length: int | None = Field(default=None, alias="seriesLength")
    short_description: str | None = Field(default=None, alias="shortDescription")
    similar_movies: list[SimilarMovie] | None = Field(default=None, alias="similarMovies")
    status: str | None = Field(default=None)
    total_series_length: int | None = Field(default=None, alias="totalSeriesLength")
    year: int | None = Field(default=None)
    kp_updated_at: datetime = Field(default=None, alias="updatedAt")
    description: str | None = Field(default=None, alias="description")
    slogan: str | None = Field(default=None, alias="slogan")
    en_name: str | None = Field(default=None, alias="enName")


class KpMediaItemsList(BaseModel):
    docs: list[KpMediaItem]


class KpMediaCollection(BaseModel):
    name: str | None = Field(default=None)
    slug: str | None = Field(default=None)
    items: list[KpMediaItem] | None = Field(default=[])


class KpMediaCollectionsList(BaseModel):
    docs: list[KpMediaCollection]

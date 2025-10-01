from enum import StrEnum
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROJECT_DOCS_PATH = PROJECT_ROOT.joinpath("docs")


class MediaType(StrEnum):
    tv_series = "tv-series"
    animated_series = "animated-series"
    cartoon = "cartoon"
    movie = "movie"
    remake = "remake"


class KpCollections(StrEnum):
    ten_greatest = "100_greatest_TVseries"
    series_about_vampires = "series_about_vampires"
    best_mini_serial = "best_mini_serial"
    popular_series = "popular-series"
    hbo_best = "hbo_best"
    series_top250 = "series-top250"
    audiodescription = "audiodescription"
    hearing_impairment = "hearing_impairment"


COLLECTIONS: dict[str, dict[str, str]] = {
    KpCollections.hbo_best: {"name": "Шедевры HBO"},
    KpCollections.popular_series: {"name": "Популярные сериалы"},
    KpCollections.ten_greatest: {"name": "100_greatest_TVseries"},
    KpCollections.series_about_vampires: {"name": "Сериалы про вампиров"},
    KpCollections.best_mini_serial: {"name": "Лучшие сериалы мини-формата"},
    KpCollections.series_top250: {"name": "250 лучших сериалов"},
    KpCollections.audiodescription: {"name": "Фильмы и сериалы с тифлокомментариями"},
    KpCollections.hearing_impairment: {"name": "Фильмы и сериалы с субтитрами для людей с особенностями слуха"},
}

FAVORITE_TIME: dict[str, list[int]] = {
    "До 2000": [1900, 2000],
    "2000-2010": [2000, 2010],
    "2010-2020": [2010, 2020],
    "2020-2025": [2020, 2030],
}

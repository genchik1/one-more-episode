from dependency_injector.wiring import Provide, inject

from src.application.di.container import StoreContainer
from src.application.services import KinopoiskDataLoaderService
from src.consts import COLLECTIONS


@inject
async def save_kinopoisk_series(
    service: KinopoiskDataLoaderService = Provide[StoreContainer.kinopoisk_data_loader_service],
) -> None:
    await service.load_series_info()


@inject
async def save_kinopoisk_collections(
    service: KinopoiskDataLoaderService = Provide[StoreContainer.kinopoisk_data_loader_service],
) -> None:
    for collection_slug in COLLECTIONS:
        await service.load_collection(str(collection_slug))

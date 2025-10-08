from dependency_injector.wiring import Provide

from src.application.di.container import StoreContainer
from src.application.services import EmbeddingsFactoryService


async def save_embeddings(
    service: EmbeddingsFactoryService = Provide[StoreContainer.embeddings_factory_service],
) -> None:
    await service.load()

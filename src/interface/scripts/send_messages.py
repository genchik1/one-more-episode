from dependency_injector.wiring import Provide, inject

from src.application.di.container import StoreContainer
from src.application.services import TelegramUserInteractionService


@inject
async def send_messages_to_bot(
    service: TelegramUserInteractionService = Provide[StoreContainer.user_interaction_service],
) -> None:
    await service.send_bookmarks(user_id=964766594)

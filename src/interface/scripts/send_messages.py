from dependency_injector.wiring import Provide, inject

from src.application.commands import MessageCommand
from src.application.di.container import StoreContainer
from src.application.services import UserInteractionService


@inject
async def send_messages_to_bot(
    service: UserInteractionService = Provide[StoreContainer.user_interaction_service],
) -> None:
    message = MessageCommand(chat_id=666301341, text="check")
    await service.send_message(message)

from src.application import commands
from src.infrastructure.external import TelegramApiClient


class UserInteractionService:
    """штукенция, которая сендит сообщения в бота"""

    # FIXME: переименовать

    def __init__(self, client: TelegramApiClient) -> None:
        self._client = client

    async def send_message(self, message: commands.MessageCommand):
        result = await self._client.send_message(message.__dict__)
        pass

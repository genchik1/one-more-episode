from src.application.commands import message as commands
from src.application.dtos import TgMessage
from src.domain.models import ItemsCollection, UserFeatures
from src.domain.models.user import TelegramFeatures
from src.domain.repositories import IDbRepository
from src.infrastructure.external import TelegramApiClient
from src.settings import TELEGRAM


class TelegramUserInteractionService:
    def __init__(self, client: TelegramApiClient, cache_repository: IDbRepository) -> None:
        self._client = client
        self._repository = cache_repository

    async def get_user_telegram_features(self, user_id: int) -> UserFeatures:
        return await self._repository.get_user_features(user_id, ["telegram_features"])

    async def send_bookmarks(self, user_id: int) -> None:
        features = await self.get_user_telegram_features(user_id)
        if features.telegram_features and features.telegram_features.is_send_bookmark_message:
            return

        message = commands.MessageWithButtonCommand(
            chat_id=user_id,
            text="Любимые сериалы всегда под рукой",
            reply_markup={"inline_keyboard": [[{"text": "Закладки", "url": TELEGRAM.bookmarks_page}]]},
        )
        result: TgMessage = await self._client.send_message(message.__dict__)

        command = commands.PinnedMessageCommand(
            chat_id=result.result.chat.id,
            message_id=result.result.message_id,
        )
        await self._client.pinned_message(command.__dict__)

        telegram_features = features.telegram_features or TelegramFeatures(is_send_bookmark_message=True)
        features.telegram_features = telegram_features
        await self._repository.save_user_features(features)

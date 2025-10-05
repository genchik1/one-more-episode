from src.application.commands.like_item import LikeItemCommand
from src.application.errors import InvalidCommandError
from src.domain.models import UserItemFeatures
from src.domain.repositories import IDbRepository


class LikeItemUseCase:
    def __init__(self, cache_repository: IDbRepository):
        self._repository = cache_repository

    async def execute(self, command: LikeItemCommand) -> None:
        if command.action not in ["like", "dislike", "bookmark", "unbookmark"]:
            raise InvalidCommandError("Invalid action")

        user_feature = UserItemFeatures(
            user_id=command.user_id,
            item_id=command.item_id,
            is_like=(command.action == "like"),
            is_dislike=(command.action == "dislike"),
            is_bookmark=(command.action == "bookmark"),
            is_unbookmark=(command.action == "unbookmark"),
        )

        await self._repository.save_user_item_features([user_feature])

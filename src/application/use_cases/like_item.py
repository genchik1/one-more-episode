from src.application.commands.like_item import LikeItemCommand
from src.application.errors import InvalidCommandError
from src.domain.logger import ILogger
from src.domain.models import UserItemFeatures
from src.domain.repositories import IDbRepository


class LikeItemUseCase:
    def __init__(self, cache_repository: IDbRepository, logger: ILogger):
        self._repository = cache_repository
        self._logger = logger

    async def execute(self, command: LikeItemCommand) -> None:
        self._logger.info(
            "action", extra={"user_id": command.user_id, "item_id": command.item_id, "action": command.action}
        )
        if command.action not in ["like", "unlike", "undislike", "dislike", "bookmark", "unbookmark"]:
            raise InvalidCommandError("Invalid action")

        user_item_feature = UserItemFeatures(
            user_id=command.user_id,
            item_id=command.item_id,
            is_like=(command.action == "like") or not (command.action == "unlike"),
            is_dislike=(command.action == "dislike") or not (command.action == "undislike"),
            is_bookmark=(command.action == "bookmark") or not (command.action == "unbookmark"),
        )

        await self._repository.save_user_item_features([user_item_feature])
        self._logger.info("saved user_item_feature")
        user_features = await self._repository.get_user_features(
            command.user_id, ["bookmarked_series", "liked_series", "disliked_series"]
        )

        match command.action:
            case "like":
                user_features.liked_series.append(command.item_id)
                if command.item_id in user_features.disliked_series:
                    user_features.disliked_series.remove(command.item_id)
            case "unlike":
                if command.item_id in user_features.liked_series:
                    user_features.liked_series.remove(command.item_id)
            case "dislike":
                user_features.disliked_series.append(command.item_id)
                if command.item_id in user_features.liked_series:
                    user_features.liked_series.remove(command.item_id)
            case "undislike":
                if command.item_id in user_features.disliked_series:
                    user_features.disliked_series.remove(command.item_id)
            case "bookmark":
                user_features.bookmarked_series.append(command.item_id)
            case "unbookmark":
                if command.item_id in user_features.bookmarked_series:
                    user_features.bookmarked_series.remove(command.item_id)

        await self._repository.save_user_features(user_features)
        self._logger.info("saved user_item_feature")

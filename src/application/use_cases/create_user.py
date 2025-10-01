from src.application import commands
from src.domain import models
from src.domain.repositories import IDbRepository


class CreateUserUseCase:
    def __init__(self, cache_repository: IDbRepository):
        self._repository = cache_repository

    async def execute(self, command: commands.CreateUserCommand) -> None:
        user_feature = models.UserFeatures(user_id=command.user_id, username=command.username)

        await self._repository.save_user_features(user_feature)

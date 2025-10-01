from src.application.errors import GetFromDBError
from src.domain.models import ItemFeatures
from src.domain.repositories import IDbRepository
from src.infrastructure.repositories.errors import ReadError


# TODO кажется это не use-case
class ItemFeaturesUseCase:
    def __init__(self, cache_repository: IDbRepository):
        self._repository = cache_repository

    async def get(self, item_id: int) -> ItemFeatures:
        try:
            return await self._repository.get_item_feature(item_id)
        except ReadError as err:
            raise GetFromDBError(str(err))

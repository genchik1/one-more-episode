from src.application import commands
from src.application.stages.errors import StageError
from src.domain import repositories
from src.domain.models import ItemsCollection
from src.domain.pipeline import IPipelineStage
from src.infrastructure.repositories.errors import ReadError


class GetUserCollectionsStage(IPipelineStage):
    def __init__(
        self,
        cache_repository: repositories.IDbRepository,
        stage_meta: commands.PersonalMetaCommand,
        target_feature: str,
        features: list[str],
    ) -> None:
        self._cache_repository = cache_repository
        self._features = features
        self._stage_meta = stage_meta
        self._target_feature = target_feature

    async def process(self, collection: ItemsCollection | None = None) -> ItemsCollection:
        if collection.items:
            return collection
        try:
            user_features = await self._cache_repository.get_user_features(
                self._stage_meta.user_id, features=[self._target_feature]
            )
        except ReadError as err:
            raise StageError from err
        collection.items = await self._cache_repository.get_item_features(
            user_features.bookmarked_series, self._features
        )
        return collection

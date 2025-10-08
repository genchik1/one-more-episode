from src.application import commands
from src.application.services import SeriesRecommendationService
from src.domain.models import ItemFeatures, ItemsCollection
from src.domain.pipeline import IPipelineStage


class GetSearchRecommendationsStage(IPipelineStage):
    def __init__(
        self, recommendation_service: SeriesRecommendationService, stage_meta: commands.StageMetaCommand
    ) -> None:
        self._recommendation_service = recommendation_service
        self._stage_meta = stage_meta

    async def process(
        self,
        collection: ItemsCollection | None = None,
    ) -> ItemsCollection:
        items: list[commands.SimilarityItemCommand] = self._recommendation_service.predict(
            self._stage_meta.search_query, self._stage_meta.count_items
        )
        return ItemsCollection(items=[ItemFeatures.model_construct(id=item.id) for item in items])

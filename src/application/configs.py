from src.application import services, stages
from src.application.commands.search_stage_meta import StageMetaCommand
from src.application.pipeline import Pipeline
from src.domain import repositories
from src.domain.logger import ILogger
from src.domain.models import ItemsCollection


def pipeline_for_kinopoisk_loader(collection: ItemsCollection) -> Pipeline:
    return Pipeline() >> stages.AddCollectionStage(collection) >> stages.FilterByRatingStage(min_rating=6)


def pipeline_get_collection(cache_repository: repositories.IDbRepository, collection_slug: str) -> Pipeline:
    features = ["id", "name", "year", "rating", "short_description"]
    min_rating = 7.0
    return (
        Pipeline()
        >> stages.GetCollectionStage(cache_repository, collection_slug, features=features)
        >> stages.FilterByRatingStage(min_rating=min_rating)
    )


def pipeline_get_onboarding_v1(
    logger: ILogger, cache_repository: repositories.IDbRepository, file_repository: repositories.IFileRepository
) -> Pipeline:
    logger.info("run onboarding pipeline")
    features = ["id", "name", "rating", "description", "poster"]
    name = "onboarding_v1"
    slug = "onboarding-v1"
    return (
        Pipeline()
        >> stages.GetOnboardingCollectionV1Stage(cache_repository, file_repository, features, name, slug)
        >> stages.FilterWithoutPreviewUrlStage()
    )


def pipeline_get_search_recommendations(
    recommendation_service: services.SeriesRecommendationService,
    cache_repository: repositories.IDbRepository,
    stage_meta: StageMetaCommand,
) -> Pipeline:
    features = ["id", "name", "rating", "description", "poster"]
    return (
        Pipeline()
        >> stages.GetSearchRecommendationsStage(recommendation_service, stage_meta)
        >> stages.LoadItemFeaturesStage(cache_repository, features)
    )

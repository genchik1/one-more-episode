from src.application import commands, services, stages
from src.application.pipeline import Pipeline
from src.consts import KpCollections
from src.domain import repositories
from src.domain.logger import ILogger
from src.domain.models import ItemsCollection

RETURN_FEATURES: list[str] = ["id", "name", "rating", "description", "poster", "year"]


def pipeline_for_kinopoisk_loader(collection: ItemsCollection) -> Pipeline:
    return Pipeline() >> stages.AddCollectionStage(collection) >> stages.FilterByRatingStage(min_rating=6)


def pipeline_get_collection(cache_repository: repositories.IDbRepository, collection_slug: str) -> Pipeline:
    features = RETURN_FEATURES
    min_rating = 7.0
    return (
        Pipeline()
        >> stages.GetCollectionStage(cache_repository, collection_slug, features=features)
        >> stages.FilterByRatingStage(min_rating=min_rating)
    )


def pipeline_get_onboarding_v1(logger: ILogger, cache_repository: repositories.IDbRepository) -> Pipeline:
    logger.info("run onboarding pipeline")
    features = RETURN_FEATURES
    return (
        Pipeline()
        >> stages.GetCollectionStage(cache_repository, KpCollections.ten_greatest, features=features)
        >> stages.FilterWithoutPreviewUrlStage()
    )


def pipeline_get_search_recommendations(
    recommendation_service: services.SeriesRecommendationService,
    cache_repository: repositories.IDbRepository,
    stage_meta: commands.StageMetaCommand,
) -> Pipeline:
    features = RETURN_FEATURES
    return (
        Pipeline()
        >> stages.GetSearchRecommendationsStage(recommendation_service, stage_meta)
        >> stages.LoadItemFeaturesStage(cache_repository, features)
    )


def pipeline_get_user_bookmarks(
    cache_repository: repositories.IDbRepository,
    stage_meta: commands.PersonalMetaCommand,
) -> Pipeline:
    features = RETURN_FEATURES
    return (
        Pipeline()
        >> stages.GetUserCollectionsStage(cache_repository, stage_meta, "bookmarked_series", features)
        >> stages.LoadItemFeaturesStage(cache_repository, features)
    )

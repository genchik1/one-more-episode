from src.application import stages
from src.application.pipeline import Pipeline
from src.domain import repositories
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
    cache_repository: repositories.IDbRepository, file_repository: repositories.IFileRepository
) -> Pipeline:
    features = ["id", "name", "year", "rating", "short_description", "poster"]
    min_rating = 6.0
    name = "onboarding_v1"
    slug = "onboarding-v1"
    return (
        Pipeline()
        >> stages.GetOnboardingCollectionV1Stage(cache_repository, file_repository, features, name, slug)
        >> stages.FilterByRatingStage(min_rating=min_rating)
    )

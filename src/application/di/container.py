from dependency_injector import containers, providers

from src.application import configs, use_cases
from src.application.services import KinopoiskDataLoaderService
from src.consts import PROJECT_DOCS_PATH
from src.infrastructure import repositories
from src.infrastructure.external.clients import init_kinopoisk_api, init_redis_media_items


class StoreContainer(containers.DeclarativeContainer):
    kinopoisk_api_client = providers.Resource(init_kinopoisk_api)
    redis_client = providers.Resource(init_redis_media_items)

    kinopoisk_repository = providers.Factory(repositories.KinopoiskRepository, kinopoisk_api_client)
    redis_repository = providers.Factory(repositories.RedisRepository, redis_client)
    kp_save_info_file_repository = providers.Factory(repositories.KinopoiskSaveInfoFileRepository)

    kinopoisk_loader_pipeline_func = providers.Callable(lambda: configs.pipeline_for_kinopoisk_loader)

    kinopoisk_data_loader_service = providers.Factory(
        KinopoiskDataLoaderService,
        kinopoisk_repository=kinopoisk_repository,
        cache_repository=redis_repository,
        file_repository=kp_save_info_file_repository,
        callable_pipeline_func=kinopoisk_loader_pipeline_func,
    )
    get_collection_pipeline = providers.Factory(
        configs.pipeline_get_collection,
        cache_repository=redis_repository,
        collection_slug=providers.Dependency(),
    )

    onboarding_json_file_repository = providers.Factory(
        repositories.JsonFileRepository, file_path=PROJECT_DOCS_PATH.joinpath("kp-api").joinpath("onboarding.json")
    )
    get_onboarding_collection_v1_pipeline = providers.Factory(
        configs.pipeline_get_onboarding_v1,
        cache_repository=redis_repository,
        file_repository=onboarding_json_file_repository,
    )

    like_item_use_case = providers.Factory(use_cases.LikeItemUseCase, cache_repository=redis_repository)
    item_features_use_case = providers.Factory(use_cases.ItemFeaturesUseCase, cache_repository=redis_repository)
    create_user_use_case = providers.Factory(use_cases.CreateUserUseCase, cache_repository=redis_repository)

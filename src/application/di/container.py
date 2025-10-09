from dependency_injector import containers, providers

from src import settings
from src.application import configs, services, use_cases
from src.consts import PROJECT_DOCS_PATH
from src.infrastructure import external, repositories
from src.infrastructure.external.clients import init_kinopoisk_api, init_redis_media_items
from src.infrastructure.log import StructuredLogger, setup_logging


class StoreContainer(containers.DeclarativeContainer):
    logging_setup = providers.Resource(setup_logging)
    logger = providers.Factory(StructuredLogger, logging_setup)

    kinopoisk_api_client = providers.Resource(init_kinopoisk_api, config=settings.KINOPOISK)
    redis_client = providers.Resource(init_redis_media_items, config=settings.REDIS, logger=logger)
    telegram_api_client = providers.Resource(
        external.TelegramApiClient,
        api_url=settings.TELEGRAM.api_url.format(token=settings.TELEGRAM.token),  # FIXME
    )

    kinopoisk_repository = providers.Factory(repositories.KinopoiskRepository, kinopoisk_api_client)
    redis_repository = providers.Factory(repositories.RedisRepository, redis_client)
    kp_save_info_file_repository = providers.Factory(
        repositories.KinopoiskSaveInfoFileRepository, config=settings.KINOPOISK
    )

    kinopoisk_loader_pipeline_func = providers.Callable(lambda: configs.pipeline_for_kinopoisk_loader)

    kinopoisk_data_loader_service = providers.Factory(
        services.KinopoiskDataLoaderService,
        config=settings.KINOPOISK,
        logger=logger,
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
        logger=logger,
        cache_repository=redis_repository,
    )

    user_interaction_service = providers.Factory(
        services.TelegramUserInteractionService,
        client=telegram_api_client,
        cache_repository=redis_repository,
    )
    like_item_use_case = providers.Factory(
        use_cases.LikeItemUseCase,
        cache_repository=redis_repository,
        logger=logger,
        user_interaction_service=user_interaction_service,
    )
    item_features_use_case = providers.Factory(use_cases.ItemFeaturesUseCase, cache_repository=redis_repository)
    create_user_use_case = providers.Factory(use_cases.CreateUserUseCase, cache_repository=redis_repository)

    embedding_provider = providers.Singleton(
        external.OllamaEmbeddingProvider, base_url=settings.ML_CONFIG.base_url, model=settings.ML_CONFIG.model
    )
    embedding_repository = providers.Singleton(
        repositories.FileEmbeddingRepository, file_path=settings.ML_CONFIG.embeddings_file
    )
    embeddings_factory_service = providers.Singleton(
        services.EmbeddingsFactoryService,
        logger=logger,
        series_repository=redis_repository,
        file_embedding=embedding_repository,
        embedding_provider=embedding_provider,
    )
    series_recommendation_service = providers.Singleton(
        services.SeriesRecommendationService,
        embeddings_factory_service=embeddings_factory_service,
        embedding_provider=embedding_provider,
    )
    get_search_recommendation_pipeline = providers.Factory(
        configs.pipeline_get_search_recommendations,
        recommendation_service=series_recommendation_service,
        cache_repository=redis_repository,
        stage_meta=providers.Dependency(),
    )
    get_user_bookmarks_pipeline = providers.Factory(
        configs.pipeline_get_user_bookmarks,
        cache_repository=redis_repository,
        stage_meta=providers.Dependency(),
    )

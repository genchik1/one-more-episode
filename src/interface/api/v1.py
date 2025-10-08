from typing import Annotated, Any

from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, HTTPException

from src.application import commands, services, use_cases
from src.application.di.container import StoreContainer
from src.application.errors import GetFromDBError, InvalidCommandError, PipelineError
from src.application.pipeline import Pipeline
from src.consts import KpCollections
from src.interface.api.dtos import LikeRequest

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


async def get_collection_pipeline_depends(slug: KpCollections) -> Pipeline:
    return await Provide[StoreContainer.get_collection_pipeline].provider(collection_slug=slug)


@router.get("/collection/{slug}")
async def get_collection(pipeline: Annotated[Pipeline, Depends(get_collection_pipeline_depends)]) -> dict[str, Any]:
    try:
        collection = await pipeline.execute()
    except PipelineError as err:
        raise HTTPException(status_code=404, detail=str(err))
    return collection.model_dump(exclude_none=True, exclude_defaults=True)


async def get_onboarding_pipeline_depends() -> Pipeline:
    return await Provide[StoreContainer.get_onboarding_collection_v1_pipeline].provider()


@router.get("/onboarding")
async def get_onboarding(pipeline: Annotated[Pipeline, Depends(get_onboarding_pipeline_depends)]) -> dict[str, Any]:
    try:
        collection = await pipeline.execute()
    except PipelineError as err:
        raise HTTPException(status_code=404, detail=str(err))
    return collection.model_dump(exclude_none=True, exclude_defaults=True)


async def get_like_item_use_case() -> use_cases.LikeItemUseCase:
    return await Provide[StoreContainer.like_item_use_case].provider()


@router.post("/like")
async def post_like(
    like_data: LikeRequest,
    use_case: Annotated[use_cases.LikeItemUseCase, Depends(get_like_item_use_case)],
):
    command = commands.LikeItemCommand(user_id=like_data.user_id, item_id=like_data.item_id, action=like_data.rating)
    try:
        await use_case.execute(command)
    except InvalidCommandError:
        raise HTTPException(status_code=422)
    except Exception:
        raise HTTPException(status_code=400)


async def get_item_features_use_case() -> use_cases.ItemFeaturesUseCase:
    return await Provide[StoreContainer.item_features_use_case].provider()


@router.get("/item/{item_id}")
async def get_item(
    item_id: int,
    use_case: Annotated[use_cases.ItemFeaturesUseCase, Depends(get_item_features_use_case)],
) -> dict[str, Any]:
    try:
        item = await use_case.get(item_id)
    except GetFromDBError:
        raise HTTPException(status_code=404)
    except Exception:
        raise HTTPException(status_code=400)

    return item.model_dump(exclude_none=True, exclude_defaults=True)


async def get_series_recommendation_service() -> use_cases.ItemFeaturesUseCase:
    return await Provide[StoreContainer.series_recommendation_service].provider()


@router.post("/search")
async def search(
    text: str,
    service: Annotated[services.SeriesRecommendationService, Depends(get_series_recommendation_service)],
):
    await service.load()
    return service.predict(text, 5)

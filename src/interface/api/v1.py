from typing import Annotated, Any

from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, HTTPException

from src.application import commands, services, use_cases
from src.application.di.container import StoreContainer
from src.application.errors import GetFromDBError, InvalidCommandError, PipelineError
from src.application.pipeline import Pipeline
from src.consts import KpCollections
from src.interface.api.dtos import LikeRequest
from src.interface.api.utils import convert_list_items_to_frontend

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


async def _get_collection_pipeline_depends(slug: KpCollections) -> Pipeline:
    return await Provide[StoreContainer.get_collection_pipeline].provider(collection_slug=slug)


@router.get("/collection/{slug}")
async def get_collection(pipeline: Annotated[Pipeline, Depends(_get_collection_pipeline_depends)]) -> dict[str, Any]:
    try:
        collection = await pipeline.execute()
    except PipelineError as err:
        raise HTTPException(status_code=404, detail=str(err))
    return collection.model_dump(exclude_none=True, exclude_defaults=True)


async def _get_onboarding_pipeline_depends() -> Pipeline:
    return await Provide[StoreContainer.get_onboarding_collection_v1_pipeline].provider()


@router.get("/onboarding")
async def get_onboarding(pipeline: Annotated[Pipeline, Depends(_get_onboarding_pipeline_depends)]) -> dict[str, Any]:
    try:
        collection = await pipeline.execute()
    except PipelineError as err:
        raise HTTPException(status_code=404, detail=str(err))
    return collection.model_dump(exclude_none=True, exclude_defaults=True)


async def _get_like_item_use_case() -> use_cases.LikeItemUseCase:
    return await Provide[StoreContainer.like_item_use_case].provider()


@router.post("/like")
async def post_like(
    like_data: LikeRequest,
    use_case: Annotated[use_cases.LikeItemUseCase, Depends(_get_like_item_use_case)],
):
    command = commands.LikeItemCommand(user_id=like_data.user_id, item_id=like_data.item_id, action=like_data.rating)
    try:
        await use_case.execute(command)
    except InvalidCommandError:
        raise HTTPException(status_code=422)
    except Exception:
        raise HTTPException(status_code=400)


async def _get_item_features_use_case() -> use_cases.ItemFeaturesUseCase:
    return await Provide[StoreContainer.item_features_use_case].provider()


@router.get("/item/{item_id}")
async def get_item(
    item_id: int,
    use_case: Annotated[use_cases.ItemFeaturesUseCase, Depends(_get_item_features_use_case)],
) -> dict[str, Any]:
    try:
        item = await use_case.get(item_id)
    except GetFromDBError:
        raise HTTPException(status_code=404)
    except Exception:
        raise HTTPException(status_code=400)

    return item.model_dump(exclude_none=True, exclude_defaults=True)


async def _get_collection_pipeline_depends(user_id: int) -> Pipeline:
    stage_meta = commands.PersonalMetaCommand(user_id=user_id)
    return await Provide[StoreContainer.get_search_recommendation_pipeline].provider(stage_meta=stage_meta)


@router.get("/search/{user_id}")
async def search(
    pipeline: Annotated[Pipeline, Depends(_get_collection_pipeline_depends)],
):
    try:
        collection = await pipeline.execute()
    except PipelineError as err:
        raise HTTPException(status_code=404, detail=str(err))
    series_data = [
        item.model_dump(exclude_none=True, exclude_defaults=True)
        for item in convert_list_items_to_frontend(collection.items)
    ]

    return {"items": series_data}


async def _get_user_bookmarks_pipeline_depends(user_id: int) -> Pipeline:
    stage_meta = commands.PersonalMetaCommand(user_id=user_id)
    return await Provide[StoreContainer.get_user_bookmarks_pipeline].provider(stage_meta=stage_meta)


@router.get("/bookmarks/{user_id}")
async def get_bookmarks(
    pipeline: Annotated[Pipeline, Depends(_get_user_bookmarks_pipeline_depends)],
) -> dict[str, Any]:
    try:
        collection = await pipeline.execute()
    except PipelineError as err:
        raise HTTPException(status_code=404, detail=str(err))

    series_data = [
        item.model_dump(exclude_none=True, exclude_defaults=True)
        for item in convert_list_items_to_frontend(collection.items)
    ]
    return {"items": series_data}

from typing import Any

from fastapi import APIRouter, HTTPException

from src.application import commands, use_cases
from src.application.di.container import StoreContainer
from src.application.errors import GetFromDBError, InvalidCommandError, PipelineError
from src.consts import KpCollections
from src.interface.api.dtos import LikeRequest

router = APIRouter()
container = StoreContainer()
container.wire(modules=[__name__])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/collection/{slug}")
async def get_collection(
    slug: KpCollections,
) -> dict[str, Any]:
    pipeline = await container.get_collection_pipeline(collection_slug=slug)
    try:
        collection = await pipeline.execute()
    except PipelineError as err:
        raise HTTPException(status_code=404, detail=str(err))
    return collection.model_dump(exclude_none=True, exclude_defaults=True, exclude_unset=True)


@router.get("/onboarding")
async def get_onboarding() -> dict[str, Any]:
    pipeline = await container.get_onboarding_collection_v1_pipeline()
    try:
        collection = await pipeline.execute()
    except PipelineError as err:
        raise HTTPException(status_code=404, detail=str(err))
    return collection.model_dump(exclude_none=True, exclude_defaults=True, exclude_unset=True)


@router.post("/like")
async def post_like(like_data: LikeRequest):
    use_case: use_cases.LikeItemUseCase = await container.like_item_use_case()
    command = commands.LikeItemCommand(user_id=like_data.user_id, item_id=like_data.item_id, action=like_data.rating)
    try:
        await use_case.execute(command)
    except InvalidCommandError:
        raise HTTPException(status_code=422)
    except Exception:
        raise HTTPException(status_code=400)


@router.get("/item/{item_id}")
async def get_item(item_id: int) -> dict[str, Any]:
    use_case: use_cases.ItemFeaturesUseCase = await container.item_features_use_case()

    try:
        item = await use_case.get(item_id)
    except GetFromDBError:
        raise HTTPException(status_code=404)
    except Exception:
        raise HTTPException(status_code=400)

    return item.model_dump(exclude_none=True, exclude_defaults=True, exclude_unset=True)

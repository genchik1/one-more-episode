from fastapi import APIRouter, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.application.di.container import StoreContainer
from src.application.errors import PipelineError
from src.consts import PROJECT_ROOT

frontend = APIRouter()
container = StoreContainer()
container.init_resources()
container.wire(modules=[__name__])

templates = Jinja2Templates(directory=PROJECT_ROOT.joinpath("templates"))
frontend.mount("/static", StaticFiles(directory=PROJECT_ROOT.joinpath("static")), name="static")


@frontend.get("/onboarding")
async def onboarding(request: Request):
    pipeline = await container.get_onboarding_collection_v1_pipeline()
    try:
        collection = await pipeline.execute()
    except PipelineError as err:
        raise HTTPException(status_code=404, detail=str(err))
    collection_data = collection.model_dump(exclude_none=True, exclude_defaults=True)
    series_data = collection_data["items"]

    return templates.TemplateResponse(
        "onboarding.html", {"request": request, "series_data": series_data, "title": "Онбординг"}
    )

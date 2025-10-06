from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.application.di.container import StoreContainer
from src.interface.api import frontend, v1

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://0.0.0.0:8000",
    "https://one-more-episode.ru",
]


def create_app() -> FastAPI:
    container = StoreContainer()
    container.wire(modules=[v1, frontend])
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
        max_age=600,
    )
    app.include_router(v1.router, prefix="/api/v1")
    app.include_router(frontend.frontend)
    app.state.container = container
    return app


app = create_app()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.interface.api.frontend import frontend
from src.interface.api.v1 import router


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Разрешить все домены
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router, prefix="/api/v1")
    app.include_router(frontend)
    return app

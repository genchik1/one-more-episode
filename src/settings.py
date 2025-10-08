from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

from src.consts import PROJECT_DOCS_PATH


class KinopoiskConfig(BaseSettings):
    x_api_key: str = Field(default="", alias="KP_X_API_KEY")
    base_url: str = "https://api.kinopoisk.dev/v1.4"
    info_file_path: Path = PROJECT_DOCS_PATH.joinpath("kinopoisk_info.txt")
    limit: int = 250


class RedisConfig(BaseSettings):
    host: str = Field(default="localhost", alias="REDIS_HOST")
    port: int = 6379
    media_item_db: int = Field(default=0, alias="REDIS_DB")


class TgConfig(BaseSettings):
    token: str = Field(default="", alias="TG_BOT_TOKEN")
    url: str = Field(default="one-more-episode.ru/", alias="TG_WEB_APP_URL")
    onboarding_page: str = "/onboarding"
    api_url: str = "https://api.telegram.org/bot{token}"


class MlConfig(BaseSettings):
    embeddings_file: Path = PROJECT_DOCS_PATH.joinpath("embedding.pkl")
    base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_URL")
    model: str = "nomic-embed-text"


KINOPOISK = KinopoiskConfig()
REDIS = RedisConfig()
TELEGRAM = TgConfig()
ML_CONFIG = MlConfig()

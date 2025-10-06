from src.infrastructure.external.clients.http_base import BaseHttpClient
from src.settings import KinopoiskConfig


def init_kinopoisk_api(config: KinopoiskConfig) -> BaseHttpClient:
    client = BaseHttpClient(_base_url=config.base_url)
    return client

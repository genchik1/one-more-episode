from src.infrastructure.external.clients.http_base import BaseHttpClient
from src.infrastructure.settings import KinopoiskConfig


def init_kinopoisk_api() -> BaseHttpClient:
    client = BaseHttpClient(_base_url=KinopoiskConfig().base_url)
    return client

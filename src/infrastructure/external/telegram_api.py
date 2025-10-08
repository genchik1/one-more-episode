from typing import Any

from src.application.dtos import KpMediaItemsList
from src.infrastructure.external.clients.http_base import BaseHttpClient


class TelegramApiClient:
    def __init__(self, api_url: str) -> None:
        self._url = api_url
        self._client = BaseHttpClient(api_url)

    async def send_message(self, data: dict[str, Any]):
        data = await self._client.request(
            method="POST", url=self._url + "/sendMessage", dto_model=KpMediaItemsList, payload=data
        )
        return data

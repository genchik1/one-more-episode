from collections.abc import Mapping
from typing import Any, Type

import aiohttp
from pydantic import BaseModel

from src.infrastructure.external.clients.errors import HttpException


class BaseHttpClient:
    def __init__(self, _base_url: str, _headers: dict[str, Any] | None = None) -> None:
        self.base_url = _base_url
        self.headers = _headers or {}
        self._client_session: aiohttp.ClientSession | None = None

    async def request(
        self,
        method: str,
        url: str,
        dto_model: Type[BaseModel],
        headers: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        data: Mapping[str, Any] | None = None,
        params: Any | None = None,
        request_params: dict[str, Any] | None = None,
    ) -> BaseModel:
        request_params = request_params or {}
        try:
            response = await self._get_session().request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                json=payload,
                data=data,
                **request_params,
            )
            if response.status != 200:
                raise HttpException(str(response.reason))
            json_response = await response.text() if response.ok else None
        except Exception as exc:
            raise HttpException from exc
        return dto_model.model_validate_json(json_response)

    def _get_session(self) -> aiohttp.ClientSession:
        if not self._client_session:
            self._client_session = aiohttp.ClientSession()
        return self._client_session

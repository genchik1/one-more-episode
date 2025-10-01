from typing import Any

from pydantic import ValidationError

from src.application.dtos import KpMediaItemsList
from src.domain.models import ItemFeatures
from src.infrastructure.external.clients.errors import HttpException
from src.infrastructure.external.clients.http_base import BaseHttpClient
from src.infrastructure.repositories.errors import LoadKinopoiskSeriesError


class KinopoiskRepository:
    def __init__(self, client: BaseHttpClient) -> None:
        self._client = client

    async def load_series(self, base_url: str, params: dict[str, Any], api_key: str) -> list[ItemFeatures]:
        try:
            data = await self._client.request(
                method="GET",
                url=base_url + "/movie",
                dto_model=KpMediaItemsList,
                params=params,
                headers={"X-API-KEY": api_key},
            )
            return [
                ItemFeatures(
                    **doc.model_dump(exclude_defaults=True, exclude_none=True, exclude_unset=True, by_alias=False)
                )
                for doc in data.docs
            ]
        except HttpException as err:
            raise LoadKinopoiskSeriesError from err

        except ValidationError as err:
            raise err

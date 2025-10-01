from typing import Any, Protocol

from src.domain.models import ItemFeatures


class IKinopoiskRepository(Protocol):
    async def load_series(self, base_url: str, params: dict[str, Any], x_api_key: str) -> list[ItemFeatures]: ...

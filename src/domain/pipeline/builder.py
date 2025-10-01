from src.domain.models import ItemsCollection


class IPipelineBuilder:
    async def execute(self) -> ItemsCollection: ...

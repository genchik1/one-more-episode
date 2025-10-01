from src.domain.models import ItemsCollection


class IPipelineStage:
    async def process(self, data: ItemsCollection | None) -> ItemsCollection: ...

from src.domain.models import ItemFeatures
from src.interface.api.dtos import ItemResponse


def convert_item_to_frontend(item: ItemFeatures) -> ItemResponse:
    return ItemResponse(
        id=item.id,
        title=item.name,
        description=item.description,
        image=item.poster.preview_url or item.poster.url,
        rating=item.rating.get("kp"),
    )


def convert_list_items_to_frontend(items: list[ItemFeatures]) -> list[ItemResponse]:
    return [convert_item_to_frontend(item) for item in items]

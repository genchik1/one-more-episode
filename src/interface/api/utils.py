from src.domain.models import ItemFeatures
from src.interface.api.dtos import ItemResponse


def convert_item_to_frontend(item: ItemFeatures) -> ItemResponse:
    return ItemResponse(
        id=item.id,
        title=item.name,
        description=item.description,
        rating=item.rating.get("kp"),
        image=item.poster.preview_url or item.poster.url,
        image_full=item.poster.url or item.poster.preview_url or item.poster.url,
    )


def convert_list_items_to_frontend(items: list[ItemFeatures]) -> list[ItemResponse]:
    return [convert_item_to_frontend(item) for item in items]

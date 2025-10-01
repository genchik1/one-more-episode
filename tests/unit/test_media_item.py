from src.domain.models import ItemFeatures


def test_transform_kp_api_item_to_media_item(item_features: ItemFeatures) -> None:
    assert item_features.id == 79429
    assert item_features.seasons_info[0].episodes_count == 10
    assert item_features.genres[0].name == "триллер"

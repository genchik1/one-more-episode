from src.application.utils import like_request_2_user_item_feature
from src.domain.models import UserItemFeatures
from src.interface.api.dtos import LikeRequest


def test_like_request_2_user_item_feature():
    like_request = LikeRequest(user_id=1, item_id=1, rating="like")
    user_item_feature = like_request_2_user_item_feature(like_request)
    assert user_item_feature == UserItemFeatures(user_id=1, item_id=1, is_like=True)

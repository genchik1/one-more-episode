from src.domain.models import UserItemFeatures
from src.interface.api.dtos import LikeRequest


def like_request_2_user_item_feature(like_request: LikeRequest) -> UserItemFeatures | None:
    user_feature = UserItemFeatures(user_id=like_request.user_id, item_id=like_request.item_id)

    match like_request.rating:
        case "like":
            user_feature.is_like = True
        case "dislike":
            user_feature.is_dislike = True
        case _:
            return None
    return user_feature

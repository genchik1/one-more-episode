import pytest

from src.application.commands import LikeItemCommand
from src.application.use_cases import LikeItemUseCase
from src.domain.models import UserFeatures
from src.infrastructure.repositories import RedisRepository


@pytest.fixture
def like_item_usecase(cache_repository: RedisRepository, logger) -> LikeItemUseCase:
    return LikeItemUseCase(cache_repository, logger)


async def test_save_like_action(like_item_usecase: LikeItemUseCase, cache_repository: RedisRepository):
    user_id = 1
    item_id_1 = 10
    item_id_2 = 20
    action = "like"
    user_features = UserFeatures(user_id=user_id, disliked_series=[item_id_1, item_id_2])
    await cache_repository.save_user_features(user_features)

    like_item_command = LikeItemCommand(user_id=user_id, item_id=item_id_1, action=action)
    await like_item_usecase.execute(like_item_command)

    user_item_feature = await cache_repository.get_user_item_features(user_id, [item_id_1], ["is_like"])
    assert user_item_feature[0].is_like
    user_feature = await cache_repository.get_user_features(user_id, ["liked_series", "disliked_series"])
    assert user_feature.liked_series == [item_id_1]
    assert user_feature.disliked_series == [item_id_2]


async def test_save_bookmarked_action(like_item_usecase: LikeItemUseCase, cache_repository: RedisRepository):
    user_id = 1
    item_id_1 = 10
    item_id_2 = 20
    action = "unbookmark"
    user_features = UserFeatures(user_id=user_id, bookmarked_series=[item_id_1, item_id_2])
    await cache_repository.save_user_features(user_features)

    like_item_command = LikeItemCommand(user_id=user_id, item_id=item_id_1, action=action)
    await like_item_usecase.execute(like_item_command)

    user_feature = await cache_repository.get_user_features(user_id, ["bookmarked_series"])
    assert user_feature.bookmarked_series == [item_id_2]


async def test_save_unlike_action(like_item_usecase: LikeItemUseCase, cache_repository: RedisRepository):
    user_id = 1
    item_id_1 = 10
    item_id_2 = 20
    action = "unlike"
    user_features = UserFeatures(user_id=user_id, liked_series=[item_id_1, item_id_2])
    await cache_repository.save_user_features(user_features)

    like_item_command = LikeItemCommand(user_id=user_id, item_id=item_id_1, action=action)
    await like_item_usecase.execute(like_item_command)

    user_item_feature = await cache_repository.get_user_item_features(user_id, [item_id_1], ["is_like"])
    assert not user_item_feature[0].is_like
    user_feature = await cache_repository.get_user_features(user_id, ["liked_series"])
    assert user_feature.liked_series == [item_id_2]

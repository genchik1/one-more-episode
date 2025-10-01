import pytest
import redis

from src.domain.models import ItemFeatures, UserFeatures, UserItemFeatures
from src.infrastructure.external.clients.redis_client import init_redis_media_items
from src.infrastructure.repositories.redis_client import RedisRepository


@pytest.fixture
def media_item_collection(media_item: ItemFeatures) -> list[ItemFeatures]:
    return [media_item]


@pytest.fixture
def user_item_features() -> list[UserItemFeatures]:
    return [
        UserItemFeatures(item_id=1, user_id=10, is_like=True),
        UserItemFeatures(item_id=2, user_id=10, is_dislike=True),
    ]


@pytest.fixture
def user_features() -> list[UserFeatures]:
    return [
        UserFeatures(user_id=10, username="test_user_10"),
        UserFeatures(user_id=20, username="test_user_20"),
    ]


@pytest.fixture
def redis_client():
    return init_redis_media_items()


async def test_redis_item_features_repository(
    redis_client: redis.Redis, media_item_collection: list[ItemFeatures]
) -> None:
    repository = RedisRepository(redis_client)
    await repository.save_item_features(media_item_collection)

    media_item_collection_ids = [item.id for item in media_item_collection]
    media_item_collection_names = [item.name for item in media_item_collection]
    media_item_collection_genres = [item.genres for item in media_item_collection]
    media_items_result = await repository.get_item_features(media_item_collection_ids, ["name", "genres"])
    assert media_items_result[0].name == media_item_collection_names[0]
    assert [genre.name for genre in media_items_result[0].genres] == [
        genre.name for genre in media_item_collection_genres[0]
    ]


async def test_redis_user_item_features_repository(
    redis_client: redis.Redis, user_item_features: list[UserItemFeatures]
) -> None:
    repository = RedisRepository(redis_client)
    await repository.save_user_item_features(user_item_features)

    user_id = 10
    item_ids = [feature_object.item_id for feature_object in user_item_features if feature_object.user_id == user_id]
    user_item_features_result = await repository.get_user_item_features(user_id, item_ids, ["is_like", "is_dislike"])
    assert user_item_features_result == user_item_features


async def test_redis_user_features_repository(redis_client: redis.Redis, user_features: list[UserFeatures]) -> None:
    repository = RedisRepository(redis_client)
    await repository.save_user_features(user_features[0])
    await repository.save_user_features(user_features[1])

    first_user = user_features[0]
    result = await repository.get_user_features(first_user.user_id, features=["username"])
    assert result.username == first_user.username

    first_user.is_viewed_series = True
    await repository.save_user_features(first_user)
    result = await repository.get_user_features(first_user.user_id, features=["username", "is_viewed_series"])
    assert result.username == first_user.username
    assert result.is_viewed_series == True

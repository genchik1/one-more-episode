from typing import Any

import orjson
import redis.asyncio as redis
from redis import RedisError

from src.domain.models import ItemFeatures, ItemsCollection, UserFeatures, UserItemFeatures
from src.infrastructure.repositories.errors import ReadError, SaveError


class RedisRepository:
    def __init__(self, client: redis.Redis) -> None:
        self._client: redis.Redis = client
        self._key_sep = "|"

    async def save_item_features(self, collection: list[ItemFeatures]) -> None:
        async with self._client.pipeline() as pipe:
            for item in collection:
                item_dict: dict[str, Any] = item.model_dump(
                    exclude_none=True,
                    exclude_defaults=True,
                )
                serialized_item_dict = {
                    ItemFeatures.replace_key(key): orjson.dumps(value) for key, value in item_dict.items()
                }
                await pipe.hset(str(item.id), mapping=serialized_item_dict)

            try:
                await pipe.execute()
            except RedisError as err:
                raise SaveError("Error saving titles info to redis") from err

    async def get_item_feature(self, identifier: int) -> ItemFeatures:
        try:
            item_result = await self._client.hgetall(str(identifier))
        except RedisError as err:
            raise ReadError("Error getting titles info from redis") from err

        media_item_data: dict[str, Any] = {"id": identifier}
        for feature, value in item_result.items():
            if value is not None:
                media_item_data[ItemFeatures.get_real_key(feature)] = orjson.loads(value)
        return ItemFeatures(**media_item_data)

    async def get_item_features(self, identifiers: list[int], features: list[str]) -> list[ItemFeatures]:
        replaced_features: list[str] = [ItemFeatures.replace_key(key) for key in features]
        async with self._client.pipeline() as pipe:
            for item_id in identifiers:
                await pipe.hmget(str(item_id), replaced_features)

            try:
                redis_results = await pipe.execute()
            except RedisError as err:
                raise ReadError("Error getting titles info from redis") from err

        collection: list[ItemFeatures] = []
        for item_id, item_result in zip(identifiers, redis_results, strict=True):
            media_item_data: dict[str, Any] = {"id": item_id}
            for feature, value in zip(features, item_result, strict=True):
                if value is not None:
                    media_item_data[feature] = orjson.loads(value)
            collection.append(ItemFeatures(**media_item_data))

        return collection

    async def save_collection(self, collection: ItemsCollection) -> None:
        try:
            await self._client.set(
                collection.slug,
                orjson.dumps(
                    collection.model_dump(
                        exclude_none=True,
                        exclude_defaults=True,
                    )
                ),
            )
        except RedisError as err:
            raise SaveError("Error saving collection to redis") from err

    async def get_collection(self, collection_slug: str) -> ItemsCollection:
        try:
            redis_results = await self._client.get(collection_slug)
        except RedisError as err:
            raise ReadError("Error getting collection from redis") from err
        if not redis_results:
            raise ReadError("not found")
        return ItemsCollection(**orjson.loads(redis_results))

    async def save_user_item_features(self, user_item_features: list[UserItemFeatures]) -> None:
        async with self._client.pipeline() as pipe:
            for user_item_feature in user_item_features:
                user_item_feature_dict: dict[str, Any] = user_item_feature.model_dump(
                    exclude_none=True,
                    exclude_defaults=True,
                )
                serialized_user_item_feature_dict = {
                    UserItemFeatures.replace_key(key): orjson.dumps(value)
                    for key, value in user_item_feature_dict.items()
                }
                await pipe.hset(
                    f"{user_item_feature.item_id}|{user_item_feature.user_id}",
                    mapping=serialized_user_item_feature_dict,
                )

            try:
                await pipe.execute()
            except RedisError as err:
                raise SaveError("Error saving user item features to redis") from err

    async def get_user_item_features(
        self, user_id: int, identifiers: list[int], features: list[str]
    ) -> list[UserItemFeatures]:
        replaced_features: list[str] = [UserItemFeatures.replace_key(key) for key in features]
        async with self._client.pipeline() as pipe:
            for item_id in identifiers:
                await pipe.hmget(f"{item_id}|{user_id}", replaced_features)

            try:
                redis_results = await pipe.execute()
            except RedisError as err:
                raise ReadError("Error getting user item features from redis") from err

        collection: list[UserItemFeatures] = []
        for item_id, item_result in zip(identifiers, redis_results, strict=True):
            media_item_data: dict[str, Any] = {"item_id": item_id, "user_id": user_id}
            for feature, value in zip(features, item_result, strict=True):
                if value is not None:
                    media_item_data[feature] = orjson.loads(value)
            collection.append(UserItemFeatures(**media_item_data))

        return collection

    async def save_user_features(self, user_feature: UserFeatures) -> None:
        user_dict: dict[str, Any] = user_feature.model_dump(
            exclude_none=True,
            exclude_defaults=True,
        )
        serialized_item_dict = {UserFeatures.replace_key(key): orjson.dumps(value) for key, value in user_dict.items()}
        try:
            await self._client.hset(f"user|{user_feature.user_id}", mapping=serialized_item_dict)
        except RedisError as err:
            raise SaveError("Error saving user features to redis") from err

    async def get_user_features(self, user_id: int, features: list[str]) -> UserFeatures:
        replaced_features: list[str] = [UserFeatures.replace_key(key) for key in features]
        redis_result = await self._client.hmget(f"user|{user_id}", replaced_features)

        user_data: dict[str, Any] = {"user_id": user_id}
        for feature, value in zip(features, redis_result, strict=True):
            if value is not None:
                user_data[feature] = orjson.loads(value)
        return UserFeatures(**user_data)

from functools import lru_cache

from pydantic import BaseModel


class UserItemFeatures(BaseModel):
    item_id: int
    user_id: int
    is_like: bool = False
    is_dislike: bool = False
    is_bookmark: bool = False
    is_unbookmark: bool = False

    @classmethod
    @lru_cache
    def get_numerated_keys(cls) -> dict[str, int]:
        return {
            "item_id": 1,
            "user_id": 2,
            "is_like": 3,
            "is_dislike": 4,
            "is_bookmark": 5,
            "is_unbookmark": 6,
        }

    @classmethod
    def replace_key(cls, key: str) -> str:
        return str(cls.get_numerated_keys()[key])

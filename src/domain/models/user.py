from functools import lru_cache

from pydantic import BaseModel, Field


class TelegramFeatures(BaseModel):
    is_send_bookmark_message: bool = False


class UserFeatures(BaseModel):
    user_id: int
    username: str | None = Field(default=None)
    is_viewed_series: bool = False
    love_genres: list[str] = Field(default=[])
    favorite_times: list[list[int]] = Field(default=[])
    bookmarked_series: list[int] = Field(default=[])
    liked_series: list[int] = Field(default=[])
    disliked_series: list[int] = Field(default=[])
    telegram_features: TelegramFeatures | None = Field(default=None)
    last_search_message: str = ""

    @classmethod
    @lru_cache
    def get_numerated_keys(cls) -> dict[str, int]:
        return {
            "user_id": 1,
            "username": 2,
            "is_viewed_series": 3,
            "love_genres": 4,
            "favorite_times": 5,
            "bookmarked_series": 6,
            "liked_series": 7,
            "disliked_series": 8,
            "telegram_features": 9,
            "last_search_message": 10,
        }

    @classmethod
    def replace_key(cls, key: str) -> str:
        return str(cls.get_numerated_keys()[key])

from pydantic import BaseModel, Field


class LikeRequest(BaseModel):
    item_id: int
    rating: str
    user_id: int = 0

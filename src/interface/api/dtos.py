from pydantic import BaseModel, Field


class LikeRequest(BaseModel):
    item_id: int
    rating: str
    user_id: int = 0


class ItemResponse(BaseModel):
    id: int
    title: str
    description: str
    rating: float
    image: str
    image_full: str

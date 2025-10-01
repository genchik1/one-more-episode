from pydantic import BaseModel


class LikeItemCommand(BaseModel):
    user_id: int
    item_id: int
    action: str  # "like" or "dislike"

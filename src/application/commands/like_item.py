from typing import NamedTuple


class LikeItemCommand(NamedTuple):
    user_id: int
    item_id: int
    action: str

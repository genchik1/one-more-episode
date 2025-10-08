from typing import NamedTuple


class CreateUserCommand(NamedTuple):
    user_id: int
    username: str

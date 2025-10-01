from pydantic import BaseModel


class CreateUserCommand(BaseModel):
    user_id: int
    username: str

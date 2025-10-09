from pydantic import BaseModel


class ChatMessageResult(BaseModel):
    id: int


class MessageResult(BaseModel):
    message_id: int
    chat: ChatMessageResult


class TgMessage(BaseModel):
    ok: bool
    result: MessageResult


class TgCallback(BaseModel):
    ok: bool
    result: bool

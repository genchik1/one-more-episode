import dataclasses
from typing import Any


# FIXME: наверное не ок что он зависит от dataclass, а остальные от NamedTuple
@dataclasses.dataclass
class MessageWithButtonCommand:
    chat_id: int
    text: str
    reply_markup: dict[str, Any]
    parse_mode: str = "MarkdownV2"
    silent: bool = True


@dataclasses.dataclass
class PinnedMessageCommand:
    chat_id: int
    message_id: int
    disable_notification: bool = True

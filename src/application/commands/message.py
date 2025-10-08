import dataclasses


# FIXME: наверное не ок что он зависит от dataclass, а остальные от NamedTuple
@dataclasses.dataclass
class MessageCommand:
    chat_id: int
    text: str
    parse_mode: str = "MarkdownV2"

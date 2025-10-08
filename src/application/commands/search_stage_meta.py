from typing import NamedTuple


class StageMetaCommand(NamedTuple):
    search_query: str
    count_items: int = 5

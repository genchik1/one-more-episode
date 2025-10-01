from typing import Any, Optional, Protocol


class IFileRepository(Protocol):
    def write(self, data: Any) -> None: ...

    def read(self) -> Optional[Any]: ...

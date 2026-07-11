from abc import abstractmethod
from typing import Any, Protocol, Sequence


class Flusher(Protocol):

    @abstractmethod
    async def flush(self, objects: Sequence[Any] | None = None) -> None:
        ...

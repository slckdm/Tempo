from abc import abstractmethod
from typing import Any, Protocol


class Cacher(Protocol):

    @abstractmethod
    async def set(self, key: str, value: Any) -> None:
        ...

    @abstractmethod
    async def get(self, key: str) -> Any:
        ...

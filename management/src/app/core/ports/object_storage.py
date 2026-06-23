from abc import abstractmethod
from typing import Protocol

from toolkit.entities.object import Object


class ObjectStorage(Protocol):

    @abstractmethod
    async def get_object(self, key: str) -> Object: ...

    @abstractmethod
    async def put_object(self, key: str, body: bytes, **kwargs) -> None: ...

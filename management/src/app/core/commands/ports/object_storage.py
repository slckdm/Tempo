from abc import abstractmethod
from typing import Protocol

from toolkit.entities.object import Object


class ObjectStorage(Protocol):

    @abstractmethod
    async def get_object(self, key: str) -> Object: ...

    @abstractmethod
    async def put_object(self, key: str, body: bytes, **kwargs) -> None: ...

    @abstractmethod
    async def make_object_upload_url(self, key: str, content_type: str) -> str: ...

    async def delete_object(self, key: str, **kwargs) -> None: ...

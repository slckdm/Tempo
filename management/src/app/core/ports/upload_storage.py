from abc import abstractmethod
from typing import Protocol

from app.core.models import Upload


class UploadStorage(Protocol):

    @abstractmethod
    async def add(self, upload: Upload): ...

    @abstractmethod
    async def get_by_id(self, id: int): ...

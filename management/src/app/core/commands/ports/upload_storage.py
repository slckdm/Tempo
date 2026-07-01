from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.core.models import Upload


class UploadStorage(Protocol):

    @abstractmethod
    async def add(self, upload: Upload): ...

    @abstractmethod
    async def get_by_id(self, id: UUID, for_update: bool = False) -> Upload | None: ...

    @abstractmethod
    async def delete(self, upload: Upload): ...

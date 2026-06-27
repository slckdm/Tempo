
from abc import abstractmethod
from datetime import datetime
from typing import Protocol, Sequence

from app.core.models import OutboxMessage


class OutboxStorage(Protocol):

    @abstractmethod
    async def add(self, message: OutboxMessage): ...

    @abstractmethod
    async def mark_as_published(self, ids: Sequence[int], published_at: datetime) -> None: ...

    @abstractmethod
    async def get_unpublished(self, limit: int) -> Sequence[OutboxMessage]: ...

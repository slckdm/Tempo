from abc import abstractmethod
from datetime import datetime
from typing import Protocol, Sequence

from toolkit.outbox.model import OutboxMessage
from toolkit.outbox.types import OutboxMessageID


class OutboxStorage(Protocol):
    @abstractmethod
    async def add(self, message: OutboxMessage): ...

    @abstractmethod
    async def get_unpublished(self, limit: int) -> Sequence[OutboxMessage]: ...

    @abstractmethod
    async def mark_as_published(
        self, ids: Sequence[OutboxMessageID], published_at: datetime
    ) -> None: ...

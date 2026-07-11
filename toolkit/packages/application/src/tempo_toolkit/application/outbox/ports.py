"""Transactional outbox ports."""

from collections.abc import Sequence
from datetime import datetime
from typing import Protocol

from .model import OutboxMessage
from .types import OutboxMessageID


class OutboxStorage(Protocol):
    """Persist and query outbox messages."""

    async def add(self, message: OutboxMessage) -> None:
        """Add an outbox message."""
        ...

    async def get_unpublished(self, limit: int) -> Sequence[OutboxMessage]:
        """Return unpublished messages."""
        ...

    async def mark_as_published(
        self, ids: Sequence[OutboxMessageID], published_at: datetime
    ) -> None:
        """Mark messages as published."""
        ...


class OutboxMessagePublisher(Protocol):
    """Publish outbox messages."""

    async def publish(self, message: OutboxMessage) -> None:
        """Publish one outbox message."""
        ...

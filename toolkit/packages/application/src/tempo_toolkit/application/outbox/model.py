"""Transactional outbox model."""

from datetime import datetime

from .types import OutboxMessageID


class OutboxMessage:
    """A message pending publication."""

    def __init__(
        self,
        *,
        id: OutboxMessageID,
        aggregate_type: str,
        aggregate_id: str | int,
        event_type: str,
        payload: dict,
        created_at: datetime,
        published_at: datetime | None = None,
    ) -> None:
        """Initialize an outbox message."""
        self.id = id
        self.aggregate_type = aggregate_type
        self.aggregate_id = aggregate_id
        self.event_type = event_type
        self.payload = payload
        self.created_at = created_at
        self.published_at = published_at

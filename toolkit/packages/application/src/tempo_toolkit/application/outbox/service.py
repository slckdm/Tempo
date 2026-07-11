"""Transactional outbox service."""

from uuid import uuid4

from tempo_toolkit.application.time import UTCTimer
from tempo_toolkit.contracts.events import EventContract
from tempo_toolkit.contracts.routing import RoutingKey

from .model import OutboxMessage
from .types import AggregateType, OutboxMessageID


class OutboxService:
    """Create messages for transactional persistence."""

    def __init__(self, timer: UTCTimer) -> None:
        """Initialize the service with a UTC time source."""
        self._timer = timer

    async def create_message(
        self,
        aggregate_type: AggregateType,
        aggregate_id: str,
        event_type: RoutingKey,
        payload: EventContract,
    ) -> OutboxMessage:
        """Create an unpublished outbox message."""
        return OutboxMessage(
            id=OutboxMessageID(uuid4()),
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=str(event_type),
            payload=payload.model_dump(mode="json"),
            created_at=self._timer.now,
        )

from dishka import Provider

from app.core.common.enums import AggregateType, EventType
from app.core.models import OutboxMessage
from app.core.ports.system_utc_timer import UTCTimer


class OutboxService(Provider):

    def __init__(self, timer: UTCTimer) -> None:
        self._timer = timer

    async def create_message(
        self,
        aggregate_type: AggregateType,
        aggregate_id: str,
        event_type: EventType,
        payload: dict
    ) -> OutboxMessage:
        return OutboxMessage(
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type,
            payload=payload,
            created_at=self._timer.now,
        )

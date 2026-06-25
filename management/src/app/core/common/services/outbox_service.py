from toolkit.messaging.contracts import MessageContract
from toolkit.messaging.routing import RoutingKey

from app.core.common.enums import AggregateType
from app.core.common.ports.utc_timer import UTCTimer
from app.core.models import OutboxMessage


class OutboxService:

    def __init__(self, timer: UTCTimer) -> None:
        self._timer = timer

    async def create_message(
        self,
        aggregate_type: AggregateType,
        aggregate_id: str,
        event_type: RoutingKey,
        payload: MessageContract
    ) -> OutboxMessage:
        return OutboxMessage(
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=str(event_type),
            payload=payload.model_dump(mode="json"),
            created_at=self._timer.now,
        )

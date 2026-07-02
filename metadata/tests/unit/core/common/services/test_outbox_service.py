from datetime import UTC, datetime
from uuid import UUID

import pytest

from toolkit.messaging.contracts import MessageContract
from toolkit.messaging.routing import RoutingKey

from app.core.common.enums import AggregateType
from app.core.common.ports.utc_timer import UTCTimer
from tests.unit.core.factories import create_outbox_service
from tests.unit.core.mock_types import FROZEN_NOW


class SampleContract(MessageContract):
    test: str


OCCURRED_AT = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
EVENT_ID = UUID("11111111-1111-1111-1111-111111111111")


@pytest.mark.asyncio
async def test_create_message_success(utc_timer: UTCTimer) -> None:
    outbox_service = create_outbox_service(utc_timer)
    aggregate_id = str(UUID("22222222-2222-2222-2222-222222222222"))

    message = await outbox_service.create_message(
        aggregate_type=AggregateType.METADATA,
        aggregate_id=aggregate_id,
        event_type=RoutingKey("some.rk"),
        payload=SampleContract(event_id=EVENT_ID, occurred_at=OCCURRED_AT, test="test_value"),
    )

    assert message.aggregate_type == AggregateType.METADATA
    assert message.aggregate_id == aggregate_id
    assert message.event_type == "rk.some.rk"
    assert message.created_at == FROZEN_NOW
    assert message.payload == {
        "schema_version": 1,
        "event_id": str(EVENT_ID),
        "occurred_at": "2026-01-02T03:04:05Z",
        "test": "test_value",
    }

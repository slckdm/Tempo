from datetime import datetime

import pytest
from faker import Faker
from freezegun import freeze_time
from toolkit.messaging.contracts import MessageContract
from toolkit.messaging.routing import RoutingKey

from app.core.common.enums.aggregate_type import AggregateType
from app.core.common.ports.utc_timer import UTCTimer
from tests.unit.core.factories import create_outbox_service


class TestContract(MessageContract):
    test: str

FREEZED_DATETIME = datetime.now()

@freeze_time(FREEZED_DATETIME)
@pytest.mark.asyncio
async def test_create_message_success(
    faker: Faker,
    utc_timer: UTCTimer
) -> None:
    outbox_service = create_outbox_service(utc_timer)
    event_id = faker.uuid4(cast_to=None)
    message = await outbox_service.create_message(
        aggregate_type=AggregateType.UPLOAD,
        aggregate_id=faker.uuid4(),
        event_type=RoutingKey("some.rk"),
        payload=TestContract(event_id=event_id, test="test_value")
    )

    assert message.event_type == "rk.some.rk"
    assert message.payload == {
        "schema_version": 1,
        "event_id": str(event_id),
        "test": "test_value",
        "occurred_at": FREEZED_DATETIME.isoformat() + "Z"
    }

from datetime import datetime

import pytest
from faker import Faker
from freezegun import freeze_time

from tempo_toolkit.application.time import UTCTimer
from tempo_toolkit.contracts.events import EventContract
from tempo_toolkit.contracts.routing import RoutingKey

from app.core.common.enums.aggregate_type import AggregateType
from tests.unit.core.factories import create_outbox_service


class StubContract(EventContract):
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
        payload=StubContract(event_id=event_id, test="test_value")
    )

    assert message.event_type == "rk.some.rk"
    assert message.payload == {
        "schema_version": 1,
        "event_id": str(event_id),
        "test": "test_value",
        "occurred_at": FREEZED_DATETIME.isoformat() + "Z"
    }

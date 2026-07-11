import pytest

from toolkit.common.ports.transaction import Transaction
from toolkit.common.ports.utc_timer import UTCTimer
from toolkit.outbox.ports.outbox_message_publisher import OutboxMessagePublisher
from toolkit.outbox.ports.outbox_storage import OutboxStorage

from app.core.commands.publish_outbox_messages import PublishOutboxMessages
from tests.unit.core.factories import create_outbox_message
from tests.unit.core.mock_types import FROZEN_NOW


def make_publish_outbox_messages_command(
    transaction: Transaction,
    outbox_storage: OutboxStorage,
    publisher: OutboxMessagePublisher,
    timer: UTCTimer,
) -> PublishOutboxMessages:
    return PublishOutboxMessages(
        transaction=transaction,
        outbox_storage=outbox_storage,
        publisher=publisher,
        timer=timer,
    )


@pytest.mark.asyncio
async def test_publish_outbox_messages_success(
    utc_timer: UTCTimer,
    outbox_storage: OutboxStorage,
    outbox_message_publisher: OutboxMessagePublisher,
    transaction: Transaction,
) -> None:
    messages = [create_outbox_message(id=1), create_outbox_message(id=2)]
    outbox_storage.get_unpublished.return_value = messages
    command = make_publish_outbox_messages_command(
        transaction=transaction,
        outbox_storage=outbox_storage,
        publisher=outbox_message_publisher,
        timer=utc_timer,
    )

    await command()

    assert outbox_message_publisher.publish.call_count == 2
    outbox_storage.mark_as_published.assert_called_once_with([1, 2], FROZEN_NOW)
    transaction.commit.assert_called_once()


@pytest.mark.asyncio
async def test_publish_outbox_messages_empty_is_noop(
    utc_timer: UTCTimer,
    outbox_storage: OutboxStorage,
    outbox_message_publisher: OutboxMessagePublisher,
    transaction: Transaction,
) -> None:
    outbox_storage.get_unpublished.return_value = []
    command = make_publish_outbox_messages_command(
        transaction=transaction,
        outbox_storage=outbox_storage,
        publisher=outbox_message_publisher,
        timer=utc_timer,
    )

    await command()

    outbox_message_publisher.publish.assert_not_called()
    outbox_storage.mark_as_published.assert_not_called()
    transaction.commit.assert_not_called()

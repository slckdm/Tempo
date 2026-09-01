from unittest.mock import call

import pytest

from tempo_toolkit.application.outbox import OutboxMessagePublisher, OutboxStorage
from tempo_toolkit.application.persistence import Transaction
from tempo_toolkit.application.time import UTCTimer

from app.core.commands.publish_outbox_messages import PublishOutboxMessages
from tests.unit.core.factories import create_outbox_message
from tests.unit.core.mock_types import FROZEN_NOW


def make_command(
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
    messages = [create_outbox_message(1), create_outbox_message(2)]
    outbox_storage.get_unpublished.return_value = messages
    command = make_command(
        transaction,
        outbox_storage,
        outbox_message_publisher,
        utc_timer,
    )

    await command()

    assert outbox_message_publisher.publish.await_args_list == [
        call(messages[0]),
        call(messages[1]),
    ]
    outbox_storage.mark_as_published.assert_awaited_once_with([1, 2], FROZEN_NOW)
    transaction.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_publish_outbox_messages_empty_is_noop(
    utc_timer: UTCTimer,
    outbox_storage: OutboxStorage,
    outbox_message_publisher: OutboxMessagePublisher,
    transaction: Transaction,
) -> None:
    outbox_storage.get_unpublished.return_value = []
    command = make_command(
        transaction,
        outbox_storage,
        outbox_message_publisher,
        utc_timer,
    )

    await command()

    outbox_message_publisher.publish.assert_not_awaited()
    outbox_storage.mark_as_published.assert_not_awaited()
    transaction.commit.assert_not_awaited()

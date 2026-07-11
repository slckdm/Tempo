import logging

from toolkit.common.ports.transaction import Transaction
from toolkit.common.ports.utc_timer import UTCTimer
from toolkit.outbox.ports.outbox_message_publisher import OutboxMessagePublisher
from toolkit.outbox.ports.outbox_storage import OutboxStorage


class PublishOutboxMessages:
    def __init__(
        self,
        transaction: Transaction,
        outbox_storage: OutboxStorage,
        publisher: OutboxMessagePublisher,
        timer: UTCTimer,
    ) -> None:
        self._transaction = transaction
        self._outbox_storage = outbox_storage
        self._timer = timer
        self._publisher = publisher

    async def __call__(self) -> None:
        messages = await self._outbox_storage.get_unpublished(50)

        if not messages:
            return

        for message in messages:
            logging.info(f"Publishing message {str(message)}")
            await self._publisher.publish(message)

        await self._outbox_storage.mark_as_published(
            [message.id for message in messages], self._timer.now
        )
        logging.info(f"Marked {len(messages)} messages as published")

        await self._transaction.commit()

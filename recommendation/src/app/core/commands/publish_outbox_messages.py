import logging

from tempo_toolkit.application.outbox import OutboxMessagePublisher, OutboxStorage
from tempo_toolkit.application.persistence import Transaction
from tempo_toolkit.application.time import UTCTimer


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

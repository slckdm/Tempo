from app.core.commands.ports.outbox_message_publisher import OutboxMessagePublisher
from app.core.commands.ports.outbox_storage import OutboxStorage
from app.core.commands.ports.transaction import Transaction
from app.core.commands.ports.utc_timer import UTCTimer


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
            await self._publisher.publish(message)

        await self._outbox_storage.mark_as_published(
            [message.id for message in messages], self._timer.now
        )
        await self._transaction.commit()

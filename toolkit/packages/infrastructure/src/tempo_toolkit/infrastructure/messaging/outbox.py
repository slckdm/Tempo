"""FastStream transactional outbox publisher."""

from faststream.rabbit import RabbitBroker, RabbitExchange

from tempo_toolkit.application.outbox import OutboxMessage, OutboxMessagePublisher


class FastStreamOutboxMessagePublisher(OutboxMessagePublisher):
    """Publish outbox messages through FastStream."""

    def __init__(self, broker: RabbitBroker, exchange: RabbitExchange) -> None:
        """Initialize the publisher with a broker and exchange."""
        self._broker = broker
        self._exchange = exchange

    async def publish(self, message: OutboxMessage) -> None:
        """Publish an outbox message."""
        await self._broker.publish(
            message=message.payload,
            routing_key=message.event_type,
            exchange=self._exchange,
            persist=True,
        )

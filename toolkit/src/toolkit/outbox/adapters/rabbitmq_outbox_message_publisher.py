from faststream.rabbit import RabbitBroker, RabbitExchange

from toolkit.outbox.model import OutboxMessage
from toolkit.outbox.ports.outbox_message_publisher import OutboxMessagePublisher


class FastStreamOutboxMessagePublisher(OutboxMessagePublisher):

    def __init__(self, broker: RabbitBroker, exchange: RabbitExchange) -> None:
        self._broker = broker
        self._exchange = exchange

    async def publish(self, message: OutboxMessage) -> None:
        await self._broker.publish(
            message=message.payload,
            routing_key=message.event_type,
            exchange=self._exchange,
            persist=True,
        )

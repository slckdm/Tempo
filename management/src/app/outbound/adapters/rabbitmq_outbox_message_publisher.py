from faststream.rabbit import RabbitBroker

from toolkit.messaging.broker import MANAGEMENT_EXCHANGE

from app.core.commands.ports.outbox_message_publisher import OutboxMessagePublisher
from app.core.models.outbox_message import OutboxMessage


class FastStreamOutboxMessagePublisher(OutboxMessagePublisher):
    def __init__(
        self,
        broker: RabbitBroker,
    ) -> None:
        self._broker = broker

    async def publish(self, message: OutboxMessage) -> None:
        await self._broker.publish(
            message=message.payload,
            routing_key=message.event_type,
            exchange=MANAGEMENT_EXCHANGE,
            persist=True,
        )

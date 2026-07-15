from faststream.rabbit import RabbitBroker

from tempo_toolkit.contracts.events import UploadCompletedEvent, UploadDeletedEvent
from tempo_toolkit.infrastructure.messaging.rabbitmq import (
    DELETE_METADATA_QUEUE,
    METADATA_EXCHANGE,
    PROCESS_METADATA_QUEUE,
)

from app.core.common.ports.metadata_proxy import MetadataProxy


class RabbitMQMetadataProxy(MetadataProxy):
    def __init__(self, broker: RabbitBroker) -> None:
        self._broker = broker

    async def process_metadata(self, data: UploadCompletedEvent) -> None:
        await self._broker.publish(
            data.model_dump(mode="json"),
            PROCESS_METADATA_QUEUE,
            METADATA_EXCHANGE,
            routing_key=PROCESS_METADATA_QUEUE.routing_key,
        )

    async def delete_metadata(self, data: UploadDeletedEvent) -> None:
        await self._broker.publish(
            data.model_dump(mode="json"),
            DELETE_METADATA_QUEUE,
            METADATA_EXCHANGE,
            routing_key=DELETE_METADATA_QUEUE.routing_key,
        )

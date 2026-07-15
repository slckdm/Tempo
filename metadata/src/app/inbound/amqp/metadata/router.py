from faststream import AckPolicy
from faststream.rabbit import RabbitRouter

from tempo_toolkit.infrastructure.messaging import (
    DELETE_METADATA_QUEUE,
    METADATA_EXCHANGE,
    PROCESS_METADATA_QUEUE,
)

from app.inbound.amqp.metadata.delete_metadata import delete_metadata
from app.inbound.amqp.metadata.process_metadata import process_metadata

router = RabbitRouter()

router.subscriber(PROCESS_METADATA_QUEUE, METADATA_EXCHANGE, ack_policy=AckPolicy.NACK_ON_ERROR)(
    process_metadata
)
router.subscriber(DELETE_METADATA_QUEUE, METADATA_EXCHANGE, ack_policy=AckPolicy.NACK_ON_ERROR)(
    delete_metadata
)

from faststream import AckPolicy
from faststream.rabbit import RabbitRouter

from tempo_toolkit.contracts.routing import UPLOAD_COMPLETED_EVENT_RK, UPLOAD_DELETED_EVENT_RK
from tempo_toolkit.infrastructure.messaging import (
    MANAGEMENT_EXCHANGE,
    METADATA_CONSUMER_QUEUE,
    METADATA_DLE,
    METADATA_DLQ,
    make_queue,
)

from app.inbound.amqp.events.dead_letter import on_dead_letter
from app.inbound.amqp.events.handle_upload_deleted_event import upload_deleted_handler
from app.inbound.amqp.events.handler_upload_completed_event import handle_upload_completed_event

router = RabbitRouter()


router.subscriber(
    make_queue(
        f"{METADATA_CONSUMER_QUEUE.name}.upload_completed_event_handler",
        UPLOAD_COMPLETED_EVENT_RK,
        METADATA_DLE,
    ),
    MANAGEMENT_EXCHANGE,
    ack_policy=AckPolicy.NACK_ON_ERROR,
)(handle_upload_completed_event)
router.subscriber(
    make_queue(
        f"{METADATA_CONSUMER_QUEUE.name}.upload_deleted_event_handler",
        UPLOAD_DELETED_EVENT_RK,
        METADATA_DLE,
    ),
    MANAGEMENT_EXCHANGE,
    ack_policy=AckPolicy.NACK_ON_ERROR,
)(upload_deleted_handler)
router.subscriber(METADATA_DLQ, METADATA_DLE)(on_dead_letter)

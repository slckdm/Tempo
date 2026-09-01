from faststream.rabbit import RabbitRouter

from tempo_toolkit.contracts.routing import METADATA_DELETED_EVENT_RK, METADATA_READY_EVENT_RK
from tempo_toolkit.infrastructure.messaging import (
    METADATA_EXCHANGE,
    RECOMMENDATIONS_CONSUMER_QUEUE,
    RECOMMENDATIONS_DLE,
    make_queue,
)

from app.inbound.amqp.events.metadata_completed_handler import upload_metadata_completed_handler
from app.inbound.amqp.events.metadata_deleted_handler import upload_metadata_deleted_handler


def make_event_router() -> RabbitRouter:
    router = RabbitRouter()
    metadata_ready_queue = make_queue(
        f"{RECOMMENDATIONS_CONSUMER_QUEUE.name}.upload_metadata_completed_handler",
        METADATA_READY_EVENT_RK,
        RECOMMENDATIONS_DLE,
    )
    metadata_deleted_queue = make_queue(
        f"{RECOMMENDATIONS_CONSUMER_QUEUE.name}.upload_metadata_deleted_handler",
        METADATA_DELETED_EVENT_RK,
        RECOMMENDATIONS_DLE,
    )
    router.subscriber(metadata_ready_queue, METADATA_EXCHANGE)(upload_metadata_completed_handler)
    router.subscriber(metadata_deleted_queue, METADATA_EXCHANGE)(upload_metadata_deleted_handler)

    return router

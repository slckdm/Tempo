from faststream.rabbit import RabbitRouter

from tempo_toolkit.contracts.routing import METADATA_FAILED_EVENT_RK, METADATA_READY_EVENT_RK
from tempo_toolkit.infrastructure.messaging import (
    MANAGEMENT_CONSUMER_QUEUE,
    MANAGEMENT_DLE,
    METADATA_EXCHANGE,
    make_queue,
)

from .upload_metadata_completed_handler import upload_metadata_completed_handler
from .upload_metadata_failed_handler import upload_metadata_failed_handler


def make_event_router() -> RabbitRouter:
    router = RabbitRouter()
    metadata_ready_queue = make_queue(
        f"{MANAGEMENT_CONSUMER_QUEUE.name}.upload_metadata_completed_handler",
        METADATA_READY_EVENT_RK,
        MANAGEMENT_DLE,
    )
    metadata_failed_queue = make_queue(
        f"{MANAGEMENT_CONSUMER_QUEUE.name}.upload_metadata_failed_handler",
        METADATA_FAILED_EVENT_RK,
        MANAGEMENT_DLE,
    )
    router.subscriber(metadata_ready_queue, METADATA_EXCHANGE)(upload_metadata_completed_handler)
    router.subscriber(metadata_failed_queue, METADATA_EXCHANGE)(upload_metadata_failed_handler)

    return router

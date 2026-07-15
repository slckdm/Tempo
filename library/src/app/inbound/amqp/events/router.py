from faststream import AckPolicy
from faststream.rabbit import RabbitRouter

from tempo_toolkit.contracts.routing import UPLOAD_DELETED_EVENT_RK
from tempo_toolkit.infrastructure.messaging import (
    LIBRARY_CONSUMER_QUEUE,
    LIBRARY_DLE,
    LIBRARY_DLQ,
    MANAGEMENT_EXCHANGE,
    make_queue,
)

from .handle_upload_deleted_event import upload_deleted_handler
from .on_dead_letter import on_dead_letter


def make_events_router() -> RabbitRouter:
    router = RabbitRouter()

    upload_deleted_queue = make_queue(
        f"{LIBRARY_CONSUMER_QUEUE.name}.upload_deleted_handler",
        UPLOAD_DELETED_EVENT_RK,
        LIBRARY_DLE,
    )

    router.subscriber(
        upload_deleted_queue, MANAGEMENT_EXCHANGE, ack_policy=AckPolicy.NACK_ON_ERROR
    )(upload_deleted_handler)
    router.subscriber(LIBRARY_DLQ, LIBRARY_DLE)(on_dead_letter)

    return router

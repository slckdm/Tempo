import logging

from dishka import FromDishka
from dishka_faststream import inject
from faststream.rabbit import RabbitMessage, RabbitRouter

from tempo_toolkit.contracts.events import MetadataFailedEvent, MetadataReadyEvent
from tempo_toolkit.contracts.routing import METADATA_FAILED_EVENT_RK, METADATA_READY_EVENT_RK
from tempo_toolkit.infrastructure.messaging import (
    MANAGEMENT_CONSUMER_QUEUE,
    MANAGEMENT_DLE,
    MANAGEMENT_DLQ,
    METADATA_EXCHANGE,
    make_queue,
)

from app.core.commands.fail_upload import FailUpload
from app.core.commands.finish_upload import FinishUpload
from app.core.common.exceptions import StatusUpdateFlowError

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


@router.subscriber(metadata_ready_queue, METADATA_EXCHANGE)
@inject
async def upload_metadata_completed_handler(
    payload: MetadataReadyEvent, handler: FromDishka[FinishUpload]
) -> None:
    try:
        await handler(payload)
    except StatusUpdateFlowError:
        return


@router.subscriber(metadata_failed_queue, METADATA_EXCHANGE)
@inject
async def upload_metadata_failed_handler(
    payload: MetadataFailedEvent, handler: FromDishka[FailUpload]
) -> None:
    try:
        await handler(payload)
    except StatusUpdateFlowError:
        return


@router.subscriber(MANAGEMENT_DLQ, MANAGEMENT_DLE)
async def on_dead_letter(msg: RabbitMessage) -> None:
    logging.warning("dead-lettered: %r", msg.body)

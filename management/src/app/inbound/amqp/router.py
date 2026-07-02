import logging

from dishka import FromDishka
from dishka_faststream import inject
from faststream.rabbit import RabbitMessage, RabbitRouter
from toolkit.messaging.broker import (
    MANAGEMENT_DLE,
    MANAGEMENT_DLQ,
    METADATA_EXCHANGE,
    make_queue,
)
from toolkit.messaging.contracts import MetadataFailedEvent, MetadataReadyEvent
from toolkit.messaging.routing import METADATA_FAILED_RK, METADATA_READY_RK

from app.core.commands.fail_upload import FailUpload
from app.core.commands.finish_upload import FinishUpload
from app.core.common.exceptions import StatusUpdateFlowError

router = RabbitRouter()

metadata_ready_queue = make_queue(str(METADATA_READY_RK), MANAGEMENT_DLE)
metadata_failed_queue = make_queue(str(METADATA_FAILED_RK), MANAGEMENT_DLE)


@router.subscriber(metadata_ready_queue, METADATA_EXCHANGE)
@inject
async def upload_metadata_completed(
    payload: MetadataReadyEvent, handler: FromDishka[FinishUpload]
) -> None:
    try:
        await handler(payload)
    except StatusUpdateFlowError:
        return


@router.subscriber(metadata_failed_queue, METADATA_EXCHANGE)
@inject
async def upload_metadata_failed(
    payload: MetadataFailedEvent, handler: FromDishka[FailUpload]
) -> None:
    try:
        await handler(payload)
    except StatusUpdateFlowError:
        return


@router.subscriber(MANAGEMENT_DLQ, MANAGEMENT_DLE)
async def on_dead_letter(msg: RabbitMessage) -> None:
    logging.warning("dead-lettered: %r", msg.body)

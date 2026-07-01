import logging

from dishka import FromDishka
from dishka_faststream import inject
from faststream import AckPolicy
from faststream.rabbit import RabbitMessage, RabbitRouter

from toolkit.messaging.broker import MANAGEMENT_EXCHANGE, METADATA_DLE, METADATA_DLQ, make_queue
from toolkit.messaging.contracts import UploadCompletedEvent, UploadDeletedEvent
from toolkit.messaging.routing import UPLOAD_COMPLETED_RK, UPLOAD_DELETED_RK
from toolkit.service.exceptions import NotFound

from app.core.commands.delete_track_metadata import DeleteTrackMetadata
from app.core.commands.fail_metadata import FailMetadata
from app.core.commands.process_track_metadata import ProcessTrackMetadata
from app.core.common.exceptions import MetadataAlreadyProcessed, TagParseError
from app.outbound.exceptions import MetadataParserError

router = RabbitRouter()

upload_completed_queue = make_queue(str(UPLOAD_COMPLETED_RK), METADATA_DLE)
upload_deleted_queue = make_queue(str(UPLOAD_DELETED_RK), METADATA_DLE)


@router.subscriber(upload_completed_queue, MANAGEMENT_EXCHANGE, ack_policy=AckPolicy.NACK_ON_ERROR)
@inject
async def process_track_metadata(
    payload: UploadCompletedEvent,
    interactor: FromDishka[ProcessTrackMetadata],
    fail_handler: FromDishka[FailMetadata],
) -> None:
    try:
        await interactor(payload)
    except MetadataAlreadyProcessed:
        return
    except (NotFound, TagParseError, MetadataParserError) as perm_exc:
        await fail_handler(payload, perm_exc)


@router.subscriber(upload_deleted_queue, MANAGEMENT_EXCHANGE, ack_policy=AckPolicy.NACK_ON_ERROR)
@inject
async def delete_track_metadata(
    payload: UploadDeletedEvent, interactor: FromDishka[DeleteTrackMetadata]
) -> None:
    try:
        await interactor(payload)
    except NotFound:
        return


@router.subscriber(METADATA_DLQ, METADATA_DLE)
async def on_dead_letter(msg: RabbitMessage) -> None:
    print("dead-lettered: %r" % msg.body)
    logging.warning("dead-lettered: %r", msg.body)

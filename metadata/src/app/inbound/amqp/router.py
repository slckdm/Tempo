import logging

from dishka import FromDishka
from dishka_faststream import inject
from faststream import AckPolicy
from faststream.rabbit import RabbitMessage, RabbitRouter

from toolkit.messaging.broker import MANAGEMENT_EXCHANGE, METADATA_DLE, METADATA_DLQ, make_queue
from toolkit.messaging.contracts import UploadCompletedEvent
from toolkit.messaging.routing import UPLOAD_COMPLETED_RK
from toolkit.s3.s3_client import NoSuchKeyException

from app.core.commands.fail_metadata import FailMetadata
from app.core.commands.process_track_metadata import ProcessTrackMetadata
from app.core.common.exceptions import MetadataAlreadyProcessed, TagParseError

router = RabbitRouter()

upload_completed_queue = make_queue(str(UPLOAD_COMPLETED_RK), METADATA_DLE)


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
    except (NoSuchKeyException, TagParseError) as perm_exc:
        await fail_handler(payload, perm_exc)


@router.subscriber(METADATA_DLQ, METADATA_DLE)
async def on_dead_letter(msg: RabbitMessage) -> None:
    print("dead-lettered: %r" % msg.body)
    logging.warning("dead-lettered: %r", msg.body)

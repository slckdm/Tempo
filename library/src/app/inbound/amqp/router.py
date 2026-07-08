import logging

from dishka import FromDishka
from dishka_faststream import inject
from faststream import AckPolicy
from faststream.rabbit import RabbitMessage, RabbitRouter

from toolkit.messaging.broker import (
    LIBRARY_CONSUMER_QUEUE,
    LIBRARY_DLE,
    LIBRARY_DLQ,
    MANAGEMENT_EXCHANGE,
    METADATA_DLE,
    make_queue,
)
from toolkit.messaging.contracts import UploadDeletedEvent
from toolkit.messaging.routing import UPLOAD_DELETED_RK

from app.core.commands.remove_track_from_favorites import RemoveTrackFromFavorites
from app.core.commands.remove_track_from_playlists import RemoveTrackFromPlaylists

router = RabbitRouter()

upload_deleted_queue = make_queue(
    f"{LIBRARY_CONSUMER_QUEUE.name}.upload_deleted_handler", UPLOAD_DELETED_RK, METADATA_DLE
)

@router.subscriber(upload_deleted_queue, MANAGEMENT_EXCHANGE, ack_policy=AckPolicy.NACK_ON_ERROR)
@inject
async def upload_deleted_handler(
    payload: UploadDeletedEvent,
    playlists_interactor: FromDishka[RemoveTrackFromFavorites],
    favorites_interactor: FromDishka[RemoveTrackFromPlaylists]
) -> None:
    await playlists_interactor(payload.upload_id)
    await favorites_interactor(payload.upload_id)



@router.subscriber(LIBRARY_DLQ, LIBRARY_DLE)
async def on_dead_letter(msg: RabbitMessage) -> None:
    logging.warning("dead-lettered: %r", msg.body)

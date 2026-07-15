from dishka import FromDishka
from dishka_faststream import inject

from tempo_toolkit.application.errors import NotFound
from tempo_toolkit.contracts.events import UploadDeletedEvent

from app.core.commands.delete_track_metadata import DeleteTrackMetadata


@inject
async def upload_deleted_handler(
    payload: UploadDeletedEvent, interactor: FromDishka[DeleteTrackMetadata]
) -> None:
    try:
        await interactor(payload)
    except NotFound:
        return

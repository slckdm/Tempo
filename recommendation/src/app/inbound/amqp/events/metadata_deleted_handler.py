from dishka_faststream import FromDishka, inject

from tempo_toolkit.contracts.events import MetadataDeletedEvent

from app.core.commands.delete_track_features import DeleteSongFeatures


@inject
async def upload_metadata_deleted_handler(
    payload: MetadataDeletedEvent, handler: FromDishka[DeleteSongFeatures]
) -> None:
    await handler(payload)

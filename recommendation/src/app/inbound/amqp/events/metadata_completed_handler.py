from dishka_faststream import FromDishka, inject

from tempo_toolkit.contracts.events import MetadataReadyEvent

from app.core.commands.save_track_features import SaveSongFeatures


@inject
async def upload_metadata_completed_handler(
    payload: MetadataReadyEvent, handler: FromDishka[SaveSongFeatures]
) -> None:
    await handler(payload)

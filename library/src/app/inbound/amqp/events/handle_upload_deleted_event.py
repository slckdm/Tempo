from dishka import FromDishka
from dishka_faststream import inject

from tempo_toolkit.contracts.events import UploadDeletedEvent

from app.core.commands.remove_track_from_favorites import RemoveTrackFromFavorites
from app.core.commands.remove_track_from_playlists import RemoveTrackFromPlaylists


@inject
async def upload_deleted_handler(
    payload: UploadDeletedEvent,
    playlists_interactor: FromDishka[RemoveTrackFromFavorites],
    favorites_interactor: FromDishka[RemoveTrackFromPlaylists]
) -> None:
    await playlists_interactor(payload.upload_id)
    await favorites_interactor(payload.upload_id)

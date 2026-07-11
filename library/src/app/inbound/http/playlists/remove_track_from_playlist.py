from dishka import FromDishka
from dishka.integrations.fastapi import inject

from tempo_toolkit.contracts.uploads import UploadURN
from tempo_toolkit.infrastructure.web import JSendSuccessfulResponse

from app.core.commands.remove_track_from_playlist import RemoveTrackFromPlaylist
from app.core.common.types import PlaylistID


@inject
async def remove_track_from_playlist(
    playlist_id: PlaylistID,
    track_id: UploadURN,
    interactor: FromDishka[RemoveTrackFromPlaylist],
) -> JSendSuccessfulResponse:
    await interactor(playlist_id, track_id)
    return JSendSuccessfulResponse()

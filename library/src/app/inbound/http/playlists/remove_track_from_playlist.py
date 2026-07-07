from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from toolkit.service.response import JSendSuccessfulResponse
from toolkit.types.urn import UploadURNType

from app.core.commands.remove_track_from_playlist import RemoveTrackFromPlaylist


@inject
async def remove_track_from_playlist(
    playlist_id: UUID, track_id: UploadURNType, interactor: FromDishka[RemoveTrackFromPlaylist]
) -> JSendSuccessfulResponse:
    await interactor(playlist_id, track_id)
    return JSendSuccessfulResponse()

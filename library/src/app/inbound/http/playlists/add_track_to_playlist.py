from dishka import FromDishka
from dishka.integrations.fastapi import inject
from pydantic import BaseModel

from tempo_toolkit.contracts.uploads import UploadURN
from tempo_toolkit.infrastructure.web import JSendSuccessfulResponse

from app.core.commands.add_track_to_playlist import AddTrackToPlaylist
from app.core.common.types import PlaylistID


class AddTrackRequestBody(BaseModel):
    track_id: UploadURN


@inject
async def add_track_to_playlist(
    playlist_id: PlaylistID, body: AddTrackRequestBody, interactor: FromDishka[AddTrackToPlaylist]
) -> JSendSuccessfulResponse:
    await interactor(playlist_id, body.track_id)
    return JSendSuccessfulResponse()

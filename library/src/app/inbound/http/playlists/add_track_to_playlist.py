from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from pydantic import BaseModel

from toolkit.service.response import JSendSuccessfulResponse
from toolkit.types.urn import UploadURNType

from app.core.commands.add_track_to_playlist import AddTrackToPlaylist


class AddTrackRequestBody(BaseModel):
    track_id: UploadURNType


@inject
async def add_track_to_playlist(
    playlist_id: UUID, body: AddTrackRequestBody, interactor: FromDishka[AddTrackToPlaylist]
) -> JSendSuccessfulResponse:
    await interactor(playlist_id, body.track_id)
    return JSendSuccessfulResponse()

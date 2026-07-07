from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from toolkit.service.response import JSendSuccessfulResponse

from app.core.queries.get_playlist import GetPlaylist
from app.core.queries.models.playlist import PlaylistQM


@inject
async def get_playlist(
    playlist_id: UUID, interactor: FromDishka[GetPlaylist]
) -> JSendSuccessfulResponse[PlaylistQM]:
    playlist = await interactor(playlist_id)

    return JSendSuccessfulResponse(data=playlist)

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from toolkit.service.response import JSendSuccessfulResponse

from app.core.commands.create_playlist import (
    CreatePlaylist,
    CreatePlaylistRequest,
    CreatePlaylistResponse,
)


@inject
async def create_playlist(
    body: CreatePlaylistRequest, interactor: FromDishka[CreatePlaylist]
) -> JSendSuccessfulResponse[CreatePlaylistResponse]:
    playlist = await interactor(body)
    return JSendSuccessfulResponse(data=playlist)

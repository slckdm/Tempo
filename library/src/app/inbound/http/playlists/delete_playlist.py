from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from toolkit.service.response import JSendSuccessfulResponse

from app.core.commands.delete_playlist import DeletePlaylist


@inject
async def delete_playlist(
    playlist_id: UUID, interactor: FromDishka[DeletePlaylist]
) -> JSendSuccessfulResponse:
    await interactor(playlist_id)
    return JSendSuccessfulResponse()

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from tempo_toolkit.infrastructure.web import JSendSuccessfulResponse

from app.core.commands.delete_playlist import DeletePlaylist
from app.core.common.types import PlaylistID


@inject
async def delete_playlist(
    playlist_id: PlaylistID, interactor: FromDishka[DeletePlaylist]
) -> JSendSuccessfulResponse:
    await interactor(playlist_id)
    return JSendSuccessfulResponse()

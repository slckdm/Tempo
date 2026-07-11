from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from tempo_toolkit.infrastructure.web import JSendSuccessfulResponse

from app.core.queries.get_playlist_tracks import GetPlaylistTracks
from app.core.queries.models.tracks import TracksQM


@inject
async def get_playlist_tracks(
    playlist_id: UUID, interactor: FromDishka[GetPlaylistTracks]
) -> JSendSuccessfulResponse[TracksQM]:
    playlist = await interactor(playlist_id)

    return JSendSuccessfulResponse(data=playlist)

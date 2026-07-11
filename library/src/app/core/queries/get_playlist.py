from tempo_toolkit.application.auth import CurrentUserService
from tempo_toolkit.application.errors import NotFound

from app.core.common.types import PlaylistID
from app.core.queries.models.playlist import PlaylistQM
from app.core.queries.ports.playlist_reader import PlaylistReader


class GetPlaylist:
    def __init__(
        self,
        playlist_reader: PlaylistReader,
        current_user_service: CurrentUserService,
    ) -> None:
        self._playlist_reader = playlist_reader
        self._current_user_service = current_user_service

    async def __call__(self, playlist_id: PlaylistID) -> PlaylistQM:
        user = await self._current_user_service.get_current_user(["tempo:etc"])
        playlist = await self._playlist_reader.get_by_id(user.id, playlist_id)

        if not playlist:
            raise NotFound

        return playlist

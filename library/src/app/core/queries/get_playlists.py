from tempo_toolkit.application.auth import CurrentUserService

from app.core.queries.models.playlists import PlaylistsQM
from app.core.queries.ports.playlist_reader import PlaylistReader
from app.core.queries.schemas.pagination import PaginationParams


class GetPlaylists:
    def __init__(
        self,
        playlist_reader: PlaylistReader,
        current_user_service: CurrentUserService,
    ) -> None:
        self._playlist_reader = playlist_reader
        self._current_user_service = current_user_service

    async def __call__(self, pagination: PaginationParams) -> PlaylistsQM:
        user = await self._current_user_service.get_current_user(["tempo:etc"])
        return await self._playlist_reader.get_list(user.id, pagination)

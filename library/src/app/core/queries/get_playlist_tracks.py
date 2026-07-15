from tempo_toolkit.application.auth import CurrentUserService

from app.core.common.types import PlaylistID
from app.core.queries.models.tracks import TracksQM
from app.core.queries.ports.tracks_reader import TrackReader


class GetPlaylistTracks:
    def __init__(
        self,
        tracks_reader: TrackReader,
        current_user_service: CurrentUserService,
    ) -> None:
        self._tracks_reader = tracks_reader
        self._current_user_service = current_user_service

    async def __call__(self, playlist_id: PlaylistID) -> TracksQM:
        user = await self._current_user_service.get_current_user(["tempo:etc"])
        return await self._tracks_reader.get_list(user.id, playlist_id)

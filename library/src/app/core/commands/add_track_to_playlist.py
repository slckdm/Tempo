from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.transaction import Transaction
from toolkit.common.services.current_user_service import CurrentUserService
from toolkit.service.exceptions import NotFound
from toolkit.types.urn import UploadURNType

from app.core.commands.ports.playlist_storage import PlaylistStorage
from app.core.commands.ports.playlist_track_storage import PlaylistTrackStorage
from app.core.common.services.playlist_service import PlaylistService
from app.core.common.services.playlist_track_service import PlaylistTrackService
from app.core.common.types import PlaylistID


class AddTrackToPlaylist:
    def __init__(
        self,
        current_user_service: CurrentUserService,
        playlist_storage: PlaylistStorage,
        playlist_track_storage: PlaylistTrackStorage,
        playlist_service: PlaylistService,
        playlist_track_service: PlaylistTrackService,
        transaction: Transaction,
        flusher: Flusher,
    ) -> None:
        self._current_user_service = current_user_service
        self._playlist_storage = playlist_storage
        self._playlist_track_storage = playlist_track_storage
        self._playlist_service = playlist_service
        self._playlist_track_service = playlist_track_service
        self._transaction = transaction
        self._flusher = flusher

    async def __call__(
        self, playlist_id: PlaylistID, track_id: UploadURNType
    ) -> None:
        user = await self._current_user_service.get_current_user(["tempo:etc"])
        playlist = await self._playlist_storage.get(user.id, playlist_id)

        if not playlist:
            raise NotFound

        track = self._playlist_track_service.create_track(playlist.id, str(track_id))
        self._playlist_service.add_track_to_playlist(playlist, track)

        await self._playlist_track_storage.add(track, playlist)

        await self._flusher.flush()
        await self._transaction.commit()

from uuid import UUID

from toolkit.service.exceptions import NotFound

from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.playlist_storage import PlaylistStorage
from app.core.commands.ports.transaction import Transaction
from app.core.common.services.current_user_service import CurrentUserService
from app.core.common.services.playlist_service import PlaylistService
from app.core.common.types import PlaylistID


class DeletePlaylist:
    def __init__(
        self,
        current_user_service: CurrentUserService,
        playlist_storage: PlaylistStorage,
        playlist_service: PlaylistService,
        transaction: Transaction,
        flusher: Flusher,
    ) -> None:
        self._current_user_service = current_user_service
        self._playlist_storage = playlist_storage
        self._playlist_service = playlist_service
        self._transaction = transaction
        self._flusher = flusher

    async def __call__(self, playlist_id: PlaylistID) -> None:
        user = await self._current_user_service.get_current_user(["tempo:etc"])

        playlist = await self._playlist_storage.get(user.id, playlist_id)

        if not playlist:
            raise NotFound

        await self._playlist_storage.delete(playlist)

        await self._flusher.flush()
        await self._transaction.commit()

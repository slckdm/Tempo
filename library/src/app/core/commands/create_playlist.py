from uuid import UUID

from pydantic import BaseModel

from toolkit.types_ import UserID

from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.playlist_storage import PlaylistStorage
from app.core.commands.ports.transaction import Transaction
from app.core.common.services.current_user_service import CurrentUserService
from app.core.common.services.playlist_service import PlaylistService


class CreatePlaylistRequest(BaseModel):
    name: str


class CreatePlaylistResponse(BaseModel):
    id: UUID
    user_id: UserID
    name: str


class CreatePlaylist:

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

    async def __call__(self, request: CreatePlaylistRequest) -> CreatePlaylistResponse:
        user = await self._current_user_service.get_current_user(["tempo:etc"])

        playlist = self._playlist_service.create_playlist(user.id, request.name)
        await self._playlist_storage.add(playlist)

        await self._flusher.flush()
        await self._transaction.commit()

        return CreatePlaylistResponse(
            id=playlist.id,
            user_id=playlist.user_id,
            name=playlist.name,
        )

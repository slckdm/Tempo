from pydantic import BaseModel

from tempo_toolkit.application.auth import CurrentUserService
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.contracts.identifiers import UserID

from app.core.commands.ports.playlist_storage import PlaylistStorage
from app.core.common.services.playlist_service import PlaylistService
from app.core.common.types import PlaylistID


class CreatePlaylistRequest(BaseModel):
    name: str


class CreatePlaylistResponse(BaseModel):
    id: PlaylistID
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

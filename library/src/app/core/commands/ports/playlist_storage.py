from abc import abstractmethod
from typing import Protocol, Sequence
from uuid import UUID

from toolkit.types_ import UserID

from app.core.models.playlist import Playlist


class PlaylistStorage(Protocol):

    @abstractmethod
    async def get(self, user_id: UserID, playlist_id: UUID) -> Playlist | None: ...

    @abstractmethod
    async def add(self, playlist: Playlist) -> None: ...

    @abstractmethod
    async def delete(self, playlist: Playlist) -> None: ...

    @abstractmethod
    async def get_list(self, user_id: UserID) -> Sequence[Playlist]: ...

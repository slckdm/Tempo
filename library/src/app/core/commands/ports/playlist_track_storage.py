from abc import abstractmethod
from typing import Protocol, Sequence
from uuid import UUID

from toolkit.types.urn import UploadURNType

from app.core.models.playlist import Playlist
from app.core.models.playlist_track import PlaylistTrack


class PlaylistTrackStorage(Protocol):

    @abstractmethod
    async def get(self, playlist_id: UUID, track_id: UploadURNType) -> PlaylistTrack | None: ...

    @abstractmethod
    async def add(self, track: PlaylistTrack, playlist: Playlist) -> None: ...

    @abstractmethod
    async def delete(self, track: PlaylistTrack) -> None: ...

    @abstractmethod
    async def get_list(self, playlist_id: UUID) -> Sequence[PlaylistTrack]: ...

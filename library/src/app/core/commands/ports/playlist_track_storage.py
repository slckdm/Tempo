from abc import abstractmethod
from typing import Protocol, Sequence, overload

from tempo_toolkit.contracts.uploads import UploadURN

from app.core.common.types import PlaylistID, TrackID
from app.core.models.playlist import Playlist
from app.core.models.playlist_track import PlaylistTrack


class PlaylistTrackStorage(Protocol):

    @abstractmethod
    async def get(
        self, playlist_id: PlaylistID, track_id: UploadURN
    ) -> PlaylistTrack | None: ...

    @abstractmethod
    async def add(self, track: PlaylistTrack, playlist: Playlist) -> None: ...

    @overload
    async def delete(self, track: PlaylistTrack) -> None: ...

    @overload
    async def delete(self, track: TrackID) -> None: ...

    @abstractmethod
    async def delete(self, track) -> None: ...

    @abstractmethod
    async def delete_all(self, track_id: UploadURN) -> None: ...

    @abstractmethod
    async def get_list(self, playlist_id: PlaylistID) -> Sequence[PlaylistTrack]: ...

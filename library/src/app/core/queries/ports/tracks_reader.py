from abc import abstractmethod
from typing import Protocol

from toolkit.types_ import UserID

from app.core.common.types import PlaylistID
from app.core.queries.models.tracks import TracksQM


class TrackReader(Protocol):
    @abstractmethod
    async def get_list(
        self, user_id: UserID, playlist_id: PlaylistID
    ) -> TracksQM: ...

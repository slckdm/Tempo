from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from toolkit.types_ import UserID

from app.core.queries.models.tracks import TracksQM


class TrackReader(Protocol):
    @abstractmethod
    async def get_list(
        self, user_id: UserID, playlist_id: UUID
    ) -> TracksQM: ...

from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from toolkit.types_ import UserID

from app.core.queries.models.playlist import PlaylistQM
from app.core.queries.models.playlists import PlaylistsQM
from app.core.queries.schemas.pagination import PaginationParams


class PlaylistReader(Protocol):

    @abstractmethod
    async def get_by_id(self, user_id: UserID, id: UUID) -> PlaylistQM | None: ...

    @abstractmethod
    async def get_list(self, user_id: UserID, pagination: PaginationParams) -> PlaylistsQM: ...

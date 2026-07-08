from abc import abstractmethod
from typing import Protocol

from toolkit.types_ import UserID

from app.core.common.types import PlaylistID
from app.core.queries.models.playlist import PlaylistQM
from app.core.queries.models.playlists import PlaylistsQM
from app.core.queries.schemas.pagination import PaginationParams


class PlaylistReader(Protocol):

    @abstractmethod
    async def get_by_id(self, user_id: UserID, id: PlaylistID) -> PlaylistQM | None: ...

    @abstractmethod
    async def get_list(self, user_id: UserID, pagination: PaginationParams) -> PlaylistsQM: ...

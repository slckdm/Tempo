from abc import abstractmethod
from typing import Protocol, Sequence
from uuid import UUID

from toolkit.types.urn import UploadURNType
from toolkit.types_ import UserID

from app.core.models.favorite import Favorite


class FavoriteStorage(Protocol):

    @abstractmethod
    async def get(self, favorite_id: UUID) -> Favorite | None: ...

    @abstractmethod
    async def get_by_user_and_track_id(
        self, user_id: UserID, track_id: UploadURNType
    ) -> Favorite | None: ...

    @abstractmethod
    async def add(self, favorite: Favorite) -> None: ...

    @abstractmethod
    async def remove(self, favorite: Favorite) -> None: ...

    @abstractmethod
    async def get_list(self, user_id: UserID) -> Sequence[Favorite]: ...

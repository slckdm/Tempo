from abc import abstractmethod
from typing import Protocol, Sequence
from uuid import UUID

from tempo_toolkit.contracts.identifiers import UserID
from tempo_toolkit.contracts.uploads import UploadURN

from app.core.models.favorite import Favorite


class FavoriteStorage(Protocol):

    @abstractmethod
    async def get(self, favorite_id: UUID) -> Favorite | None: ...

    @abstractmethod
    async def get_by_user_and_track_id(
        self, user_id: UserID, track_id: UploadURN
    ) -> Favorite | None: ...

    @abstractmethod
    async def add(self, favorite: Favorite) -> None: ...

    @abstractmethod
    async def remove(self, favorite: Favorite) -> None: ...

    @abstractmethod
    async def remove_all(self, track_id: UploadURN) -> None: ...

    @abstractmethod
    async def get_list(self, user_id: UserID) -> Sequence[Favorite]: ...

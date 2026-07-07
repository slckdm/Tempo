from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from toolkit.types_ import UserID

from app.core.queries.models.favorite import FavoriteQM
from app.core.queries.models.favorites import FavoritesQM


class FavoriteReader(Protocol):

    @abstractmethod
    async def get_list(self, user_id: UserID) -> FavoritesQM: ...

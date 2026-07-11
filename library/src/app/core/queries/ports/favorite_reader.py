from abc import abstractmethod
from typing import Protocol

from tempo_toolkit.contracts.identifiers import UserID

from app.core.queries.models.favorites import FavoritesQM


class FavoriteReader(Protocol):

    @abstractmethod
    async def get_list(self, user_id: UserID) -> FavoritesQM: ...

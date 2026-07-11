from tempo_toolkit.application.auth import CurrentUserService

from app.core.queries.models.favorites import FavoritesQM
from app.core.queries.ports.favorite_reader import FavoriteReader


class GetFavorites:

    def __init__(
        self,
        favorite_reader: FavoriteReader,
        current_user_service: CurrentUserService,
    ) -> None:
        self._favorite_reader = favorite_reader
        self._current_user_service = current_user_service

    async def __call__(self) -> FavoritesQM:
        user = await self._current_user_service.get_current_user(["tempo:etc"])
        return await self._favorite_reader.get_list(user.id)

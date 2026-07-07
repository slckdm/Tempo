from uuid import UUID

from toolkit.service.exceptions import Forbidden, NotFound

from app.core.commands.ports.favorite_storage import FavoriteStorage
from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.transaction import Transaction
from app.core.common.services.current_user_service import CurrentUserService


class RemoveFavorite:
    def __init__(
        self,
        favorite_storage: FavoriteStorage,
        flusher: Flusher,
        transaction: Transaction,
        current_user_service: CurrentUserService,
    ) -> None:
        self._favorite_storage = favorite_storage
        self._flusher = flusher
        self._transaction = transaction
        self._current_user_service = current_user_service

    async def __call__(self, favorite_id: UUID) -> None:
        user = await self._current_user_service.get_current_user(["tempo:etc"])

        favorite = await self._favorite_storage.get(favorite_id)
        if not favorite:
            raise NotFound
        if favorite.user_id != user.id:
            raise Forbidden

        await self._favorite_storage.remove(favorite)

        await self._flusher.flush()
        await self._transaction.commit()

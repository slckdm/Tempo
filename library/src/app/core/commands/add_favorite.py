from pydantic import BaseModel

from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.transaction import Transaction
from toolkit.common.services.current_user_service import CurrentUserService
from toolkit.service.exceptions import ResourceAlreadyExists
from toolkit.types.urn import UploadURNType

from app.core.commands.ports.favorite_storage import FavoriteStorage
from app.core.common.services.favorite_service import FavoriteService


class AddFavoriteRequest(BaseModel):
    """Request model for adding a favorite."""

    track_id: UploadURNType


class AddFavoriteResponse(BaseModel):
    """Response model for adding a favorite."""

    track_id: UploadURNType


class AddFavorite:
    def __init__(
        self,
        favorite_service: FavoriteService,
        flusher: Flusher,
        transaction: Transaction,
        favorite_storage: FavoriteStorage,
        current_user_service: CurrentUserService,
    ) -> None:
        self._favorite_service = favorite_service
        self._flusher = flusher
        self._transaction = transaction
        self._favorite_storage = favorite_storage
        self._current_user_service = current_user_service

    async def __call__(self, request: AddFavoriteRequest) -> AddFavoriteResponse:
        user = await self._current_user_service.get_current_user(["tempo:etc"])
        existing_favorite = await self._favorite_storage.get_by_user_and_track_id(
            user_id=user.id, track_id=request.track_id
        )

        if existing_favorite:
            raise ResourceAlreadyExists

        favorite = self._favorite_service.create_favorite(user.id, request.track_id)
        await self._favorite_storage.add(favorite)

        await self._flusher.flush()
        await self._transaction.commit()
        return AddFavoriteResponse(track_id=request.track_id)

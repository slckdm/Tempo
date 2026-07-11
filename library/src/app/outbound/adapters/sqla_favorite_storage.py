from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from toolkit.types.urn import UploadURNType
from toolkit.types_ import UserID

from app.core.commands.ports.favorite_storage import FavoriteStorage
from app.core.common.types import FavoriteID
from app.core.models.favorite import Favorite
from app.outbound.sqlalchemy.mappings.favorite import favorite_table as table


class SQLAFavoriteStorage(FavoriteStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, favorite_id: FavoriteID) -> Favorite | None:
        return await self._session.get(Favorite, favorite_id)

    async def get_by_user_and_track_id(
        self, user_id: UserID, track_id: UploadURNType
    ) -> Favorite | None:
        favorites = await self._session.scalar(
            select(Favorite).where(
                table.c.user_id == str(user_id), table.c.track_id == str(track_id)
            )
        )
        return favorites

    async def add(self, favorite: Favorite) -> None:
        self._session.add(favorite)

    async def remove(self, favorite: Favorite) -> None:
        await self._session.delete(favorite)

    async def remove_all(self, track_id: UploadURNType) -> None:
        await self._session.execute(delete(Favorite).where(table.c.track_id == str(track_id)))

    async def get_list(self, user_id: UserID) -> Sequence[Favorite]:
        return (await self._session.scalars(select(Favorite))).all()

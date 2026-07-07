from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from toolkit.types_ import UserID

from app.core.models.favorite import Favorite as table
from app.core.queries.models.favorite import FavoriteQM
from app.core.queries.models.favorites import FavoritesQM
from app.core.queries.ports.favorite_reader import FavoriteReader
from app.outbound.exceptions import FavoriteReaderError


class SQLAFavoriteReader(FavoriteReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_list(self, user_id: UserID) -> FavoritesQM:
        query = select(
            table.id,
            table.user_id,
            table.track_id,
        ).where(table.user_id == user_id)

        try:
            result = await self._session.execute(query)
            rows = result.all()
        except SQLAlchemyError as sqla_err:
            raise FavoriteReaderError from sqla_err

        return FavoritesQM(
            favorites=[
                FavoriteQM(
                    id=row.id,
                    user_id=row.user_id,
                    track_id=row.track_id,
                )
                for row in rows
            ]
        )

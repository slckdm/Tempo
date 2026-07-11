from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from tempo_toolkit.contracts.identifiers import UserID

from app.core.queries.models.favorite import FavoriteQM
from app.core.queries.models.favorites import FavoritesQM
from app.core.queries.ports.favorite_reader import FavoriteReader
from app.outbound.exceptions import FavoriteReaderError
from app.outbound.sqlalchemy.mappings.favorite import favorite_table as table


class SQLAFavoriteReader(FavoriteReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_list(self, user_id: UserID) -> FavoritesQM:
        query = select(
            table.c.id,
            table.c.user_id,
            table.c.track_id,
        ).where(table.c.user_id == user_id)

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

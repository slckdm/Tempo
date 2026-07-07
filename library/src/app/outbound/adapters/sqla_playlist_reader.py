from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from toolkit.types_ import UserID

from app.core.models.playlist import Playlist as table
from app.core.models.playlist_track import PlaylistTrack as track_table
from app.core.queries.models.playlist import PlaylistQM
from app.core.queries.models.playlists import PlaylistsQM
from app.core.queries.ports.playlist_reader import PlaylistReader
from app.core.queries.schemas.pagination import PaginationParams
from app.outbound.exceptions import PlaylistReaderError


class SQLAPlaylistReader(PlaylistReader):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UserID, id: UUID) -> PlaylistQM | None:
        query = (
            select(
                table.id,
                table.user_id,
                table.name,
                func.count(track_table.id).label("tracks_count"),
            )
            .outerjoin(track_table, track_table.playlist_id == table.id)
            .where(table.user_id == user_id, table.id == id)
            .group_by(table.id, table.user_id, table.name)
        )

        try:
            result = await self._session.execute(query)
            row = result.one_or_none()
        except SQLAlchemyError as sqla_err:
            raise PlaylistReaderError from sqla_err

        if not row:
            return None

        return PlaylistQM(
            id=row.id,
            user_id=row.user_id,
            name=row.name,
            tracks_count=row.tracks_count,
        )

    async def get_list(self, user_id: UserID, pagination: PaginationParams) -> PlaylistsQM:
        whereclause = [table.user_id == user_id]
        query = (
            select(
                table.id,
                table.user_id,
                table.name,
                func.count(track_table.id).label("tracks_count"),
                func.count().over().label("total"),
            )
            .outerjoin(track_table, track_table.playlist_id == table.id)
            .where(*whereclause)
            .group_by(table.id, table.user_id, table.name)
            .offset(pagination.offset)
            .limit(pagination.limit)
        )

        try:
            result = await self._session.execute(query)
            rows = result.all()
        except SQLAlchemyError as sqla_err:
            raise PlaylistReaderError from sqla_err

        if not rows:
            result = await self._session.execute(
                select(func.count().label("total")).where(*whereclause)
            )
            total = result.one().total
            return PlaylistsQM(
                playlists=[], total=total, offset=pagination.offset, limit=pagination.limit
            )

        return PlaylistsQM(
            playlists=[
                PlaylistQM(
                    id=row.id,
                    user_id=row.user_id,
                    name=row.name,
                    tracks_count=row.tracks_count,
                ) for row in rows
            ],
            total=rows[0].total,
            limit=pagination.limit,
            offset=pagination.offset,
        )

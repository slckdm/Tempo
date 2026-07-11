from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from tempo_toolkit.contracts.identifiers import UserID

from app.core.queries.models.tracks import TracksQM
from app.core.queries.ports.tracks_reader import TrackReader
from app.outbound.exceptions import TrackReaderError
from app.outbound.sqlalchemy.mappings.playlist import playlists_table as playlist_table
from app.outbound.sqlalchemy.mappings.playlist_track import playlists_tracks_table as table


class SQLATrackReader(TrackReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_list(self, user_id: UserID, playlist_id: UUID) -> TracksQM:
        query = (
            select(table.c.track_id)
            .where(
                (playlist_table.c.id == playlist_id) & (playlist_table.c.user_id == user_id)
            )
            .order_by(table.c.id)
            .join(playlist_table, playlist_table.c.id==table.c.playlist_id)
        )
        try:
            result = await self._session.execute(query)
            rows = result.all()
        except SQLAlchemyError as sqla_err:
            raise TrackReaderError from sqla_err

        return TracksQM(tracks=[row.track_id for row in rows])

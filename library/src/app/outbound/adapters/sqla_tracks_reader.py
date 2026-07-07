from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from toolkit.types_ import UserID

from app.core.models.playlist import Playlist as playlist_table
from app.core.models.playlist_track import PlaylistTrack as table
from app.core.queries.models.tracks import TracksQM
from app.core.queries.ports.tracks_reader import TrackReader
from app.outbound.exceptions import TrackReaderError


class SQLATrackReader(TrackReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_list(self, user_id: UserID, playlist_id: UUID) -> TracksQM:
        query = select(table.track_id).where(
            table.playlist.has(
                (playlist_table.id == playlist_id)
                & (playlist_table.user_id == user_id)
            )
        )

        try:
            result = await self._session.execute(query)
            rows = result.all()
        except SQLAlchemyError as sqla_err:
            raise TrackReaderError from sqla_err

        return TracksQM(tracks=[row.track_id for row in rows])

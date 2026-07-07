from typing import Protocol, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from toolkit.types.urn import UploadURNType

from app.core.commands.ports.playlist_track_storage import PlaylistTrackStorage
from app.core.models.playlist import Playlist
from app.core.models.playlist_track import PlaylistTrack


class SQLAPlaylistTrackStorage(PlaylistTrackStorage):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, playlist_id: UUID, track_id: UploadURNType) -> PlaylistTrack | None:
        return await self._session.scalar(
            select(PlaylistTrack).where(
                PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.track_id == str(track_id)
            )
        )

    async def add(self, track: PlaylistTrack, playlist: Playlist) -> None:
        self._session.add(track)

    async def delete(self, track: PlaylistTrack) -> None:
        await self._session.delete(track)

    async def get_list(self, playlist_id: UUID) -> Sequence[PlaylistTrack]:
        result = await self._session.scalars(
            select(PlaylistTrack).where(PlaylistTrack.playlist_id == playlist_id)
        )
        return result.all()

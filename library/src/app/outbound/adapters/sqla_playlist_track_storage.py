from typing import Sequence
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from tempo_toolkit.contracts.uploads import UploadURN

from app.core.commands.ports.playlist_track_storage import PlaylistTrackStorage
from app.core.common.types import PlaylistID, TrackID
from app.core.models.playlist import Playlist
from app.core.models.playlist_track import PlaylistTrack


class SQLAPlaylistTrackStorage(PlaylistTrackStorage):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, playlist_id: PlaylistID, track_id: UploadURN) -> PlaylistTrack | None:
        return await self._session.scalar(
            select(PlaylistTrack).where(
                PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.track_id == str(track_id)
            )
        )

    async def add(self, track: PlaylistTrack, playlist: Playlist) -> None:
        self._session.add(track)

    async def delete(self, track: PlaylistTrack | TrackID) -> None:
        if isinstance(track, PlaylistTrack):
            await self._session.delete(track)
        elif isinstance(track, UUID):
            await self._session.execute(
                delete(PlaylistTrack).where(PlaylistTrack.id == track)
            )

    async def delete_all(self, track_id: UploadURN) -> None:
        await self._session.execute(
            delete(PlaylistTrack).where(PlaylistTrack.track_id == str(track_id))
        )

    async def get_list(self, playlist_id: PlaylistID) -> Sequence[PlaylistTrack]:
        result = await self._session.scalars(
            select(PlaylistTrack).where(PlaylistTrack.playlist_id == playlist_id)
        )
        return result.all()

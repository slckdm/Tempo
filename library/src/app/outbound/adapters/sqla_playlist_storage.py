from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tempo_toolkit.contracts.identifiers import UserID

from app.core.commands.ports.playlist_storage import PlaylistStorage
from app.core.models.playlist import Playlist
from app.outbound.sqlalchemy.mappings.playlist import playlists_table as table


class SQLAPlaylistStorage(PlaylistStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, user_id: UserID, playlist_id: UUID) -> Playlist | None:
        return await self._session.scalar(
            select(Playlist).where(table.c.id == playlist_id, table.c.user_id == user_id)
        )

    async def add(self, playlist: Playlist) -> None:
        self._session.add(playlist)

    async def delete(self, playlist: Playlist) -> None:
        await self._session.delete(playlist)

    async def get_list(self, user_id: UserID) -> Sequence[Playlist]:
        result = await self._session.scalars(select(Playlist).where(table.c.user_id == user_id))
        return result.all()

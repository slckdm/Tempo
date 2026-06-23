from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from toolkit.types.enum import UploadStatus

from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.models import TrackMetadata


class SQLAMetadataStorage(MetadataStorage):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, metadata: TrackMetadata) -> None:
        self._session.add(metadata)

    async def get_by_id(self, id: UUID) -> TrackMetadata | None:
        return await self._session.get(TrackMetadata, id)

    async def list_by_filter(
        self,
        offset: int,
        limit: int,
        title: str | None = None,
        artist: str | None = None,
        album: str | None = None,
        genre: str | None = None,
    ) -> tuple[int, Sequence[TrackMetadata]]:
        whereclause = [TrackMetadata.processing_status == UploadStatus.COMPLETED]

        if title:
            whereclause.append(TrackMetadata.title.ilike(f"%{title}%"))
        if artist:
            whereclause.append(TrackMetadata.artist.ilike(f"%{artist}%"))
        if album:
            whereclause.append(TrackMetadata.album.ilike(f"%{album}%"))
        if genre:
            whereclause.append(TrackMetadata.genre.ilike(f"%{genre}%"))

        query = select(TrackMetadata).where(*whereclause)
        return (
            (await self._session.scalar(select(func.count()).select_from(query))) or 0,
            (await self._session.scalars(query.limit(limit).offset(offset))).all()
        )

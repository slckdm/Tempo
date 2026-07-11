from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.models.track_metadata import TrackMetadata


class SQLAMetadataStorage(MetadataStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, metadata: TrackMetadata) -> None:
        self._session.add(metadata)

    async def get_by_id(self, id: UUID, for_update: bool = False) -> TrackMetadata | None:
        return await self._session.get(TrackMetadata, id, with_for_update=for_update)

    async def delete(self, metadata: TrackMetadata) -> None:
        await self._session.delete(metadata)

from uuid import UUID

from tempo_toolkit.application.auth import CurrentUserService
from tempo_toolkit.application.errors import NotFound

from app.core.queries.models.metadata import MetadataQM
from app.core.queries.ports.metadata_reader import MetadataReader


class GetTrackMetadata:
    def __init__(
        self,
        metadata_reader: MetadataReader,
        current_user_service: CurrentUserService,
    ) -> None:
        self._metadata_reader = metadata_reader
        self._current_user_service = current_user_service

    async def __call__(self, upload_id: UUID) -> MetadataQM:
        await self._current_user_service.get_current_user(["tempo:etc"])
        metadata = await self._metadata_reader.get_by_id(upload_id)
        if not metadata:
            raise NotFound
        return metadata

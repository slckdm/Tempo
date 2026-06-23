from uuid import UUID

from toolkit.service.exceptions import NotFoundException

from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.common.services.current_user_service import CurrentUserService
from app.core.common.services.metadata_service import MetadataService
from app.core.models.track_metadata import TrackMetadata


class GetTrackMetadata:

    def __init__(
        self,
        metadata_service: MetadataService,
        metadata_storage: MetadataStorage,
        current_user_service: CurrentUserService,
    ) -> None:
        self._metadata_service = metadata_service
        self._metadata_storage = metadata_storage
        self._current_user_service = current_user_service

    async def __call__(self, upload_id: UUID) -> TrackMetadata:
        await self._current_user_service.get_current_user()
        metadata = await self._metadata_storage.get_by_id(upload_id)
        if not metadata:
            raise NotFoundException
        return metadata

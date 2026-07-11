from tempo_toolkit.application.auth import CurrentUserService

from app.core.common.services.metadata_service import MetadataService
from app.core.queries.models.list_metadata import ListMetadataQM
from app.core.queries.ports.metadata_reader import FilterParams, MetadataReader
from app.core.queries.schemas.pagination import PaginationParams


class GetTracksMetadata:
    def __init__(
        self,
        metadata_service: MetadataService,
        metadata_reader: MetadataReader,
        current_user_service: CurrentUserService,
    ) -> None:
        self._metadata_service = metadata_service
        self._metadata_reader = metadata_reader
        self._current_user_service = current_user_service

    async def __call__(
        self, filters: FilterParams, pagination: PaginationParams
    ) -> ListMetadataQM:
        await self._current_user_service.get_current_user(["tempo:etc"])
        return await self._metadata_reader.list_by_filter(filters, pagination)

from dataclasses import dataclass
from typing import Sequence

from pydantic import BaseModel, Field

from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.common.services.current_user_service import CurrentUserService
from app.core.common.services.metadata_service import MetadataService
from app.core.models import TrackMetadata


@dataclass
class TracksMetadataFilterResult:
    metadata: Sequence[TrackMetadata]
    total: int


class FilterParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, le=100)
    title: str | None = Field(None)
    artist: str | None = Field(None)
    album: str | None = Field(None)
    genre: str | None = Field(None)


class GetTracksMetadata:
    def __init__(
        self,
        metadata_service: MetadataService,
        metadata_storage: MetadataStorage,
        current_user_service: CurrentUserService,
    ) -> None:
        self._metadata_service = metadata_service
        self._metadata_storage = metadata_storage
        self._current_user_service = current_user_service

    async def __call__(self, filters: FilterParams) -> TracksMetadataFilterResult:
        await self._current_user_service.get_current_user()
        total, metadata = await self._metadata_storage.list_by_filter(
            offset=filters.offset,
            limit=filters.limit,
            title=filters.title,
            artist=filters.artist,
            album=filters.album,
            genre=filters.genre,
        )
        return TracksMetadataFilterResult(metadata=metadata, total=total)

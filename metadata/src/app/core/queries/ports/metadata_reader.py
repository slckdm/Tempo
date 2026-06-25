from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from app.core.queries.models.list_metadata import ListMetadataQM
from app.core.queries.models.metadata import MetadataQM
from app.core.queries.schemas.pagination import PaginationParams


@dataclass(frozen=True, slots=True)
class FilterParams:
    title: str | None
    artist: str | None
    album: str | None
    genre: str | None


class MetadataReader(Protocol):

    @abstractmethod
    async def list_by_filter(
        self, filters: FilterParams, pagination: PaginationParams
    ) -> ListMetadataQM:
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> MetadataQM | None:
        ...

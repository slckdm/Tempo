from abc import abstractmethod
from typing import Protocol, Sequence
from uuid import UUID

from app.core.models import TrackMetadata


class MetadataStorage(Protocol):

    @abstractmethod
    async def add(self, metadata: TrackMetadata) -> None:
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> TrackMetadata | None:
        ...

    @abstractmethod
    async def list_by_filter(
        self,
        /,
        offset: int,
        limit: int,
        title: str | None = None,
        artist: str | None = None,
        album: str | None = None,
        genre: str | None = None,
    ) -> tuple[int, Sequence[TrackMetadata]]:
        ...

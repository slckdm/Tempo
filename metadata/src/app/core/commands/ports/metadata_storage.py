from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.core.models import TrackMetadata


class MetadataStorage(Protocol):

    @abstractmethod
    async def add(self, metadata: TrackMetadata) -> None:
        ...

    async def get_by_id(self, id: UUID, for_update: bool = False) -> TrackMetadata | None:
        ...

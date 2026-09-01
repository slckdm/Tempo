from abc import abstractmethod
from typing import Protocol

from app.core.common.entities.collection_metadata import CollectionMetadata
from app.core.common.enums.collections import Collections


class FeatureStorage(Protocol):
    @abstractmethod
    async def save(
        self,
        collection: Collections,
        id: str,
        vector: list[int | float],
        metadata: CollectionMetadata,
    ) -> None: ...

    @abstractmethod
    async def delete(self, collection: str, *id: str) -> None:
        ...

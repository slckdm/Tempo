from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.core.common.entities.similarity import Similarity
from app.core.common.enums.collections import Collections


class FeatureReader(Protocol):
    @abstractmethod
    async def get_similar(self, collection: Collections, id: UUID) -> list[Similarity]: ...

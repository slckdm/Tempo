from abc import abstractmethod
from io import BytesIO
from typing import Protocol

from app.core.common.entities.metadata import Metadata


class MetadataParser(Protocol):

    @abstractmethod
    async def read(self, bytes: BytesIO) -> Metadata:
        ...

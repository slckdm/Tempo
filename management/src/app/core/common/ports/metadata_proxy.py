from abc import abstractmethod
from typing import Protocol

from tempo_toolkit.contracts.events import UploadCompletedEvent, UploadDeletedEvent


class MetadataProxy(Protocol):

    @abstractmethod
    async def process_metadata(self, data: UploadCompletedEvent) -> None: ...

    @abstractmethod
    async def delete_metadata(self, data: UploadDeletedEvent) -> None: ...

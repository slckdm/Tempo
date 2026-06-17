from abc import abstractmethod
from typing import Protocol

from app.core.common.entities.audio_object import AudioObject


class AudioStorage(Protocol):

    @abstractmethod
    async def get(self, key: str, range_header: str | None) -> AudioObject:
        ...

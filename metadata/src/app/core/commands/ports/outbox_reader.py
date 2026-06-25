
from abc import abstractmethod
from typing import Protocol, Sequence

from app.core.models import OutboxMessage


class OutboxReader(Protocol):

    @abstractmethod
    async def get_unpublished(self, limit: int) -> Sequence[OutboxMessage]: ...

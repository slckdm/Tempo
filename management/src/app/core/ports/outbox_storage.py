from abc import abstractmethod
from typing import Protocol

from app.core.models import OutboxMessage


class OutboxStorage(Protocol):

    @abstractmethod
    async def add(self, message: OutboxMessage): ...

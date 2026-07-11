from abc import abstractmethod
from typing import Protocol

from toolkit.outbox.model import OutboxMessage


class OutboxMessagePublisher(Protocol):
    @abstractmethod
    async def publish(self, message: OutboxMessage) -> None: ...

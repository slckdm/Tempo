from abc import abstractmethod
from typing import Protocol

from app.core.models.outbox_message import OutboxMessage


class OutboxMessagePublisher(Protocol):

    @abstractmethod
    async def publish(self, message: OutboxMessage) -> None:
        ...

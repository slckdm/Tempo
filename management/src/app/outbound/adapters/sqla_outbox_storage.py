from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import OutboxMessage
from app.core.ports.outbox_storage import OutboxStorage


class SQLAOutboxStorage(OutboxStorage):

    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, message: OutboxMessage) -> None:
        self.__session.add(message)

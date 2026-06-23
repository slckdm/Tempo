from datetime import datetime
from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import OutboxMessage
from app.core.ports.outbox_storage import OutboxStorage


class SQLAOutboxStorage(OutboxStorage):

    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, message: OutboxMessage) -> None:
        self.__session.add(message)

    async def get_unpublished(self, limit: int) -> Sequence[OutboxMessage]:
        query = (
            select(OutboxMessage)
            .where(OutboxMessage.published_at.is_(None))
            .limit(limit)
            .order_by(OutboxMessage.id)
            .with_for_update(skip_locked=True)
        )

        return (await self.__session.scalars(query)).all()

    async def mark_as_published(self, ids: Sequence[int], published_at: datetime) -> None:
        await self.__session.execute(
            update(OutboxMessage)
            .where(OutboxMessage.id.in_(ids))
            .values(published_at=published_at)
        )

from datetime import datetime
from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from toolkit.outbox.model import OutboxMessage
from toolkit.outbox.ports.outbox_storage import OutboxStorage
from toolkit.outbox.table import OutboxTable
from toolkit.outbox.types import OutboxMessageID
from toolkit.service.exceptions import OutboxStorageError


class SQLAOutboxStorage(OutboxStorage):
    def __init__(self, session: AsyncSession, table: OutboxTable) -> None:
        self.__session = session
        self.__table = table

    async def add(self, message: OutboxMessage) -> None:
        self.__session.add(message)

    async def get_unpublished(self, limit: int) -> Sequence[OutboxMessage]:
        table = self.__table
        query = (
            select(OutboxMessage)
            .where(table.c.published_at.is_(None))
            .limit(limit)
            .order_by(table.c.id)
            .with_for_update(skip_locked=True)
        )
        try:
            return (await self.__session.scalars(query)).all()
        except SQLAlchemyError as sqlalchemy_err:
            raise OutboxStorageError from sqlalchemy_err

    async def mark_as_published(
        self, ids: Sequence[OutboxMessageID], published_at: datetime
    ) -> None:
        table = self.__table
        try:
            await self.__session.execute(
                update(table).where(table.c.id.in_(ids)).values(published_at=published_at)
            )
        except SQLAlchemyError as sqlalchemy_err:
            raise OutboxStorageError from sqlalchemy_err

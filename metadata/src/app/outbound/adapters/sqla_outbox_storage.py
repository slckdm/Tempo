from datetime import datetime
from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.ports.outbox_storage import OutboxStorage
from app.core.models import OutboxMessage
from app.outbound.exceptions import OutboxStorageError


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
        try:
            return (await self.__session.scalars(query)).all()
        except SQLAlchemyError as sqlalchemy_err:
            raise OutboxStorageError from sqlalchemy_err

    async def mark_as_published(self, ids: Sequence[int], published_at: datetime) -> None:
        try:
            await self.__session.execute(
                update(OutboxMessage)
                .where(OutboxMessage.id.in_(ids))
                .values(published_at=published_at)
            )
        except SQLAlchemyError as sqlalchemy_err:
            raise OutboxStorageError from sqlalchemy_err

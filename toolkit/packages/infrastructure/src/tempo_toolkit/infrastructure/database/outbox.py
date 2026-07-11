"""SQLAlchemy transactional outbox integration."""

from collections.abc import Sequence
from datetime import datetime
from typing import NewType

from sqlalchemy import (
    JSON,
    UUID,
    Column,
    DateTime,
    Index,
    String,
    Table,
    orm,
    select,
    text,
    update,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from tempo_toolkit.application.errors import OutboxStorageError
from tempo_toolkit.application.outbox import OutboxMessage, OutboxMessageID, OutboxStorage

OutboxTable = NewType("OutboxTable", Table)


def make_outbox_message_table(registry: orm.registry) -> OutboxTable:
    """Create the shared outbox table mapping."""
    table = Table(
        "outbox_messages",
        registry.metadata,
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column("aggregate_type", String, nullable=False),
        Column("aggregate_id", UUID, nullable=False),
        Column("event_type", String, nullable=False),
        Column("payload", JSON, nullable=False),
        Column("created_at", DateTime(timezone=True), nullable=False),
        Column("published_at", DateTime(timezone=True), nullable=True),
        Index(
            "ix_outbox_messages_unpublished_id",
            "id",
            postgresql_where=text("published_at IS NULL"),
        ),
    )
    return OutboxTable(table)


class SQLAlchemyOutboxStorage(OutboxStorage):
    """Persist outbox messages with SQLAlchemy."""

    def __init__(self, session: AsyncSession, table: OutboxTable) -> None:
        """Initialize the adapter with a session and mapped table."""
        self.__session = session
        self.__table = table

    async def add(self, message: OutboxMessage) -> None:
        """Add an outbox message to the session."""
        self.__session.add(message)

    async def get_unpublished(self, limit: int) -> Sequence[OutboxMessage]:
        """Lock and return unpublished messages."""
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
        except SQLAlchemyError as sqlalchemy_error:
            raise OutboxStorageError from sqlalchemy_error

    async def mark_as_published(
        self, ids: Sequence[OutboxMessageID], published_at: datetime
    ) -> None:
        """Mark selected messages as published."""
        table = self.__table
        try:
            await self.__session.execute(
                update(table).where(table.c.id.in_(ids)).values(published_at=published_at)
            )
        except SQLAlchemyError as sqlalchemy_error:
            raise OutboxStorageError from sqlalchemy_error

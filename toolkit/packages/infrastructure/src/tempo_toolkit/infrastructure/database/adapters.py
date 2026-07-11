"""SQLAlchemy application adapters."""

from collections.abc import Sequence
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from tempo_toolkit.application.errors import TransactionError
from tempo_toolkit.application.persistence import Flusher, Transaction


class SQLAlchemyFlusher(Flusher):
    """Flush through an SQLAlchemy session."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the adapter with an SQLAlchemy session."""
        self.__session = session

    async def flush(self, objects: Sequence[Any] | None = None) -> None:
        """Flush pending session changes."""
        await self.__session.flush(objects)


class SQLAlchemyTransaction(Transaction):
    """SQLAlchemy transaction boundary."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the adapter with an SQLAlchemy session."""
        self.__session = session

    async def commit(self) -> None:
        """Commit the session transaction."""
        try:
            await self.__session.commit()
        except SQLAlchemyError as sqlalchemy_error:
            raise TransactionError from sqlalchemy_error

    async def rollback(self) -> None:
        """Roll back the session transaction."""
        try:
            await self.__session.rollback()
        except SQLAlchemyError as sqlalchemy_error:
            raise TransactionError from sqlalchemy_error

"""Module: Async database session factory."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from management.core.db import async_session, engine


async def get_db_session() -> AsyncGenerator[async_sessionmaker[AsyncSession]]:
    """Get database session factory."""
    yield async_session
    await engine.dispose()

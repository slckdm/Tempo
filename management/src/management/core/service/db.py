"""Module: Database."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine("postgresql+asyncpg://scott:tiger@localhost/")
async_session = async_sessionmaker(engine)


async def get_db_session() -> AsyncGenerator[async_sessionmaker[AsyncSession]]:
    """Get database session factory."""
    yield async_session
    await engine.dispose()

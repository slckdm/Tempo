"""Module: Database."""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from management.core.configs import DBConfig

engine = create_async_engine(DBConfig.url)
async_session = async_sessionmaker(engine)

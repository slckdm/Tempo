from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from toolkit.config.settings import PostgresSettings


class PostgresProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_async_engine(
        self,
        postgres: PostgresSettings,
    ) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(postgres.dsn)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    async def provide_async_sessionfactory(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def provide_async_session(
        self, factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with factory() as session:
            yield session

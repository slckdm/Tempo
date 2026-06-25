"""Module: Async database session factory."""

from collections.abc import AsyncIterator
from typing import Sequence

from dishka import Provider, Scope, provide
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from toolkit.clients import KeycloakClient, KeycloakConfig
from toolkit.s3 import S3Client

from app.main.config.loader import PostgresSettings
from app.main.config.settings import KeycloakSettings, RedisSettings, S3Settings


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


class KeycloakClientProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def new_client(self, config: KeycloakSettings) -> KeycloakClient:
        return KeycloakClient(
            KeycloakConfig(
                url=config.URL,
                realm=config.REALM,
                client_id=config.CLIENT_ID,
                client_secret=config.CLIENT_SECRET,
                token_url=config.token_url,
            )
        )


class RedisClientProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_redis_client(self, settings: RedisSettings) -> Redis:
        client = Redis(
            host=settings.HOST,
            port=settings.PORT,
            db=settings.DB,
            password=settings.PASSWORD,
            decode_responses=True,
            encoding="utf-8",
        )

        return client


class S3Provider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_client(self, config: S3Settings) -> S3Client:
        return S3Client(
            region_name=config.REGION_NAME,
            url=config.URL,
            access_key_id=config.ACCESS_KEY,
            secret_access_key=config.SECRET_KEY,
        )


def get_outbound_providers() -> Sequence[Provider]:
    return (
        PostgresProvider(),
        KeycloakClientProvider(),
        RedisClientProvider(),
        S3Provider(),
    )

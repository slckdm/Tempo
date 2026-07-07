from collections.abc import AsyncIterator
from typing import Sequence

from fastapi.security import OAuth2, OAuth2PasswordBearer

from dishka import Provider, Scope, collect, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from toolkit.clients import KeycloakClient, KeycloakConfig
from toolkit.s3 import S3Client

from app.core.common.auth.service import AuthorizationService
from app.main.config.loader import PostgresSettings
from app.main.config.settings import KeycloakSettings, S3Settings


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


class AuthProvider(Provider):
    scope = Scope.REQUEST

    @provide(provides=OAuth2)
    def provide_bearer_schema(self, config: KeycloakSettings) -> OAuth2PasswordBearer:
        return OAuth2PasswordBearer(
            tokenUrl=config.token_url,
            auto_error=False,
            scopes={"tempo:etc": "Access to etc endpoints"}
        )

    auth_schemas = collect(OAuth2)
    auth_service = provide(AuthorizationService)


def get_outbound_providers() -> Sequence[Provider]:
    return (
        KeycloakClientProvider(),
        PostgresProvider(),
        S3Provider(),
        AuthProvider(),
    )

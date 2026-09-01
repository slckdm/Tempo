from typing import Sequence

from fastapi.security import OAuth2PasswordBearer
from fastapi.security.base import SecurityBase

from dishka import Provider, Scope, collect, provide
from qdrant_client import AsyncQdrantClient

from tempo_toolkit.application.auth import TokenProvider
from tempo_toolkit.infrastructure.cache import RedisClientProvider
from tempo_toolkit.infrastructure.database import OutboxTable, PostgresProvider
from tempo_toolkit.infrastructure.identity import KeycloakClientProvider, KeycloakSettings
from tempo_toolkit.infrastructure.object_storage import S3Provider
from tempo_toolkit.infrastructure.web import FastAPITokenProvider

from app.main.config.settings import QdrantSettings
from app.outbound.sqlalchemy.mappings.outbox_message import outbox_messages_table


class OutboxProvider(Provider):
    scope = Scope.REQUEST

    @provide(provides=OutboxTable)
    def provide_table(self) -> OutboxTable:
        return outbox_messages_table


class AuthProvider(Provider):
    scope = Scope.REQUEST

    @provide(provides=SecurityBase)
    def provide_bearer_schema(self, config: KeycloakSettings) -> OAuth2PasswordBearer:
        return OAuth2PasswordBearer(
            tokenUrl=config.token_url,
            auto_error=False,
            scopes={"tempo:etc": "Access to etc endpoints"}
        )

    auth_schemas = collect(SecurityBase)
    token_provider = provide(FastAPITokenProvider, provides=TokenProvider)


class QdrantClientProvider(Provider):
    scope = Scope.REQUEST

    @provide(provides=AsyncQdrantClient)
    def provide_qdrant_client(self, config: QdrantSettings) -> AsyncQdrantClient:
        return AsyncQdrantClient(host=config.HOST, port=config.PORT)


def get_outbound_providers() -> Sequence[Provider]:
    return (
        KeycloakClientProvider(),
        AuthProvider(),
        RedisClientProvider(),
        PostgresProvider(),
        OutboxProvider(),
        S3Provider(),
        QdrantClientProvider()
    )

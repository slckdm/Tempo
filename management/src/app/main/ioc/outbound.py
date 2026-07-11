from typing import Sequence

from dishka import Provider, Scope, collect, provide
from fastapi.security import OAuth2, OAuth2PasswordBearer
from toolkit.common.services.authorization_service import AuthorizationService
from toolkit.config.settings import KeycloakSettings
from toolkit.outbox.table import OutboxTable
from toolkit.providers.keycloak_client_provider import KeycloakClientProvider
from toolkit.providers.postgres_provider import PostgresProvider
from toolkit.providers.redis_provider import RedisClientProvider
from toolkit.providers.s3_provider import S3Provider

from app.outbound.sqlalchemy.mappings.oubox_message import outbox_messages_table


class OutboxProvider(Provider):
    scope = Scope.REQUEST

    @provide(provides=OutboxTable)
    def provide_table(self) -> OutboxTable:
        return outbox_messages_table


class AuthProvider(Provider):
    scope = Scope.REQUEST

    @provide(provides=OAuth2)
    def provide_bearer_schema(self, config: KeycloakSettings) -> OAuth2PasswordBearer:
        return OAuth2PasswordBearer(tokenUrl=config.token_url, auto_error=False)

    auth_schemas = collect(OAuth2)
    auth_service = provide(AuthorizationService)


def get_outbound_providers() -> Sequence[Provider]:
    return (
        KeycloakClientProvider(),
        RedisClientProvider(),
        AuthProvider(),
        PostgresProvider(),
        S3Provider(),
        OutboxProvider(),
    )

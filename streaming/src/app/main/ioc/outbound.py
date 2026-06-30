"""Module: S3 Client."""

from typing import Sequence

from fastapi.security import OAuth2

from dishka import Provider, Scope, collect, provide

from toolkit.clients import KeycloakClient, KeycloakConfig
from toolkit.s3 import S3Client

from app.core.common.auth.service import AuthorizationService
from app.core.common.security.schemas import get_cookie_schema, get_oauth2_schema
from app.main.config.settings import KeycloakSettings, S3Settings


class S3Provider(Provider):
    scope = Scope.APP

    @provide
    def get_client(self, config: S3Settings) -> S3Client:
        return S3Client(
            region_name=config.REGION_NAME,
            url=config.URL,
            access_key_id=config.ACCESS_KEY,
            secret_access_key=config.SECRET_KEY,
        )


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


class AuthProvider(Provider):
    scope = Scope.REQUEST

    oauth2_schema = provide(get_cookie_schema, provides=OAuth2)
    cookie_schema = provide(get_oauth2_schema, provides=OAuth2)
    auth_schemas = collect(OAuth2)
    auth_serivce = provide(AuthorizationService)


def get_outbound_providers() -> Sequence[Provider]:
    return (S3Provider(), AuthProvider(), KeycloakClientProvider())

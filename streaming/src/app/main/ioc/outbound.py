"""Module: S3 Client."""

from typing import Sequence

from dishka import Provider, Scope, provide

from toolkit.clients import KeycloakClient, KeycloakConfig
from toolkit.s3 import S3Client

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


def get_outbound_providers() -> Sequence[Provider]:
    return (S3Provider(), KeycloakClientProvider())

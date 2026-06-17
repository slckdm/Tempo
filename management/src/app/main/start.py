"""Module: Service application factory."""

from http import HTTPStatus

from fastapi import FastAPI

from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka

from toolkit.s3.s3_client import NoSuchKeyException
from toolkit.service.exceptions import ForbiddenException, UnauthorizedException

from app.core.common import handlers
from app.inbound.http.uploads.router import make_uploads_router
from app.main.config.loader import (
    load_app_settings,
    load_keycloak_settings,
    load_postgres_settings,
    load_s3_settings,
    load_sqlalchemy_settings,
)
from app.main.config.settings import (
    AppSettings,
    KeycloakSettings,
    PostgresSettings,
    S3Settings,
    SQLAlchemySettings,
)
from app.main.ioc.provider_regisrty import get_providers
from app.outbound.keycloak_client_provider import KeycloakClientProvider
from app.outbound.providers import get_outbound_providers


def create_service() -> FastAPI:
    """Create a service."""
    # initialize service

    app_settings = load_app_settings()
    postgres_settings = load_postgres_settings()
    keycloak_settings = load_keycloak_settings()
    s3_settings = load_s3_settings()
    sqlalchemy_settings = load_sqlalchemy_settings()

    app = FastAPI(
        title=app_settings.NAME,
        exception_handlers={
            HTTPStatus.UNAUTHORIZED: handlers.unauthorized_error_handler,
            HTTPStatus.FORBIDDEN: handlers.forbidden_error_handler,
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE: handlers.unsupported_media_error_handler,
            HTTPStatus.UNPROCESSABLE_CONTENT: handlers.validation_error_handler,
            HTTPStatus.NOT_FOUND: handlers.not_found_error_handler,
            HTTPStatus.INTERNAL_SERVER_ERROR: handlers.internal_server_error_handler,
            UnauthorizedException: handlers.unauthorized_error_handler,
            ForbiddenException: handlers.forbidden_error_handler,
            NoSuchKeyException: handlers.no_such_key_error_handler,
        },
        routes=[*make_uploads_router().routes],
    )

    container = make_async_container(
        KeycloakClientProvider(),
        FastapiProvider(),
        *get_providers(),
        *get_outbound_providers(),
        context={
            PostgresSettings: postgres_settings,
            SQLAlchemySettings: sqlalchemy_settings,
            KeycloakSettings: keycloak_settings,
            S3Settings: s3_settings,
            AppSettings: app_settings,
        },
    )

    setup_dishka(container, app)

    return app


service = create_service()

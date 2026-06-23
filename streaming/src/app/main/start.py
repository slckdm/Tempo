from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka

from toolkit.s3.s3_client import NoSuchKeyException
from toolkit.service.exceptions import ForbiddenException, NotFoundException, UnauthorizedException

from app.core.common import handlers
from app.inbound.http.stream.router import make_stream_router
from app.main.config.loader import load_app_settings, load_keycloak_settings, load_s3_settings
from app.main.config.settings import AppSettings, KeycloakSettings, S3Settings
from app.main.ioc.core import CoreProvider
from app.main.ioc.provider_registry import get_providers
from app.outbound.keycloak_client_provider import KeycloakClientProvider
from app.outbound.providers import get_outbound_providers


def create_service() -> FastAPI:
    app_settings = load_app_settings()
    s3_settings = load_s3_settings()
    keycloak_settings = load_keycloak_settings()
    app = FastAPI(
        debug=app_settings.DEBUG,
        title=app_settings.NAME,
        routes=[*make_stream_router().routes],
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
            NotFoundException: handlers.not_found_error_handler,
        },
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.ALLOWED_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    container = make_async_container(
        KeycloakClientProvider(),
        CoreProvider(),
        FastapiProvider(),
        *get_providers(),
        *get_outbound_providers(),
        context={
            AppSettings: app_settings,
            S3Settings: s3_settings,
            KeycloakSettings: keycloak_settings,
        },
    )
    setup_dishka(container, app)

    return app


if __name__ == "__main__":
    import uvicorn

    app_settings = load_app_settings()

    uvicorn.run(app=create_service(), port=app_settings.PORT)

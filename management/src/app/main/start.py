"""Module: Service application factory."""

from http import HTTPStatus

from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from toolkit.service.exceptions import Forbidden, Unauthorized, UnsupportedMediaType

from app.core.common.jsend_error_handler import JsendErrorHandler, JsendFailHandler
from app.inbound.http.uploads.router import make_uploads_router
from app.main.config.loader import (
    load_app_settings,
    load_keycloak_settings,
    load_postgres_settings,
    load_redis_settings,
    load_s3_settings,
    load_sqlalchemy_settings,
)
from app.main.config.settings import (
    AppSettings,
    KeycloakSettings,
    PostgresSettings,
    RedisSettings,
    S3Settings,
    SQLAlchemySettings,
)
from app.main.ioc.outbound import get_outbound_providers


def create_service() -> FastAPI:
    """Create a service."""
    # initialize service
    app_settings = load_app_settings()
    postgres_settings = load_postgres_settings()
    keycloak_settings = load_keycloak_settings()
    s3_settings = load_s3_settings()
    sqlalchemy_settings = load_sqlalchemy_settings()
    redis_settings = load_redis_settings()

    app = FastAPI(
        debug=app_settings.DEBUG,
        title=app_settings.NAME,
        exception_handlers={
            HTTPStatus.UNAUTHORIZED: JsendErrorHandler(HTTPStatus.UNAUTHORIZED),
            HTTPStatus.FORBIDDEN: JsendErrorHandler(HTTPStatus.FORBIDDEN),
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE: JsendErrorHandler(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE
            ),
            HTTPStatus.UNPROCESSABLE_CONTENT: JsendErrorHandler(HTTPStatus.UNPROCESSABLE_CONTENT),
            HTTPStatus.NOT_FOUND: JsendErrorHandler(HTTPStatus.NOT_FOUND),
            HTTPStatus.INTERNAL_SERVER_ERROR: JsendFailHandler(HTTPStatus.INTERNAL_SERVER_ERROR),
            Unauthorized: JsendErrorHandler(HTTPStatus.UNAUTHORIZED),
            Forbidden: JsendErrorHandler(HTTPStatus.FORBIDDEN),
            UnsupportedMediaType: JsendErrorHandler(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
        },
        routes=[*make_uploads_router().routes],
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.ALLOWED_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    container = make_async_container(
        FastapiProvider(),
        *get_outbound_providers(),
        context={
            PostgresSettings: postgres_settings,
            SQLAlchemySettings: sqlalchemy_settings,
            KeycloakSettings: keycloak_settings,
            S3Settings: s3_settings,
            AppSettings: app_settings,
            RedisSettings: redis_settings,
        },
    )

    setup_dishka(container, app)

    return app


if __name__ == "__main__":
    import uvicorn

    app_settings = load_app_settings()

    uvicorn.run(app=create_service(), host=app_settings.HOST, port=app_settings.PORT)

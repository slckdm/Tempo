"""Module: Service application factory."""

from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka

from tempo_toolkit.application.errors import (
    Forbidden,
    NotFound,
    ResourceAlreadyExists,
    Unauthorized,
)
from tempo_toolkit.infrastructure.cache import RedisSettings
from tempo_toolkit.infrastructure.database import PostgresSettings, SQLAlchemySettings
from tempo_toolkit.infrastructure.identity import KeycloakSettings
from tempo_toolkit.infrastructure.web import AppSettings, JSendErrorHandler, JSendFailHandler

from app.inbound.http.v1_router import make_v1_router
from app.main.config.loader import (
    load_app_settings,
    load_keycloak_settings,
    load_logging_settings,
    load_postgres_settings,
    load_redis_settings,
    load_sqlalchemy_settings,
)
from app.main.ioc.core import CoreProvider
from app.main.ioc.outbound import get_outbound_providers
from app.main.setup import setup_logging
from app.outbound.sqlalchemy.mappings.all import map_tables


def create_service() -> FastAPI:
    """Create a service."""
    # initialize service
    logging_settings = load_logging_settings()

    setup_logging(level=logging_settings.LEVEL)

    map_tables()
    app_settings = load_app_settings()
    postgres_settings = load_postgres_settings()
    keycloak_settings = load_keycloak_settings()
    sqlalchemy_settings = load_sqlalchemy_settings()
    redis_settings = load_redis_settings()

    app = FastAPI(
        debug=app_settings.DEBUG,
        title=app_settings.NAME,
        exception_handlers={
            HTTPStatus.UNAUTHORIZED: JSendFailHandler(HTTPStatus.UNAUTHORIZED),
            HTTPStatus.FORBIDDEN: JSendFailHandler(HTTPStatus.FORBIDDEN),
            HTTPStatus.NOT_FOUND: JSendFailHandler(HTTPStatus.NOT_FOUND),
            HTTPStatus.INTERNAL_SERVER_ERROR: JSendErrorHandler(HTTPStatus.INTERNAL_SERVER_ERROR),
            Unauthorized: JSendFailHandler(HTTPStatus.UNAUTHORIZED),
            Forbidden: JSendFailHandler(HTTPStatus.FORBIDDEN),
            NotFound: JSendFailHandler(HTTPStatus.NOT_FOUND),
            ResourceAlreadyExists: JSendFailHandler(HTTPStatus.CONFLICT),
        },
        routes=[*make_v1_router().routes],
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
        CoreProvider(),
        *get_outbound_providers(),
        context={
            PostgresSettings: postgres_settings,
            SQLAlchemySettings: sqlalchemy_settings,
            KeycloakSettings: keycloak_settings,
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

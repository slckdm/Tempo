from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka

from toolkit.service.exceptions import Forbidden, NotFound, Unauthorized

from app.core.common.jsend_error_handler import JsendErrorHandler, JsendFailHandler
from app.inbound.http.stream.router import make_stream_router
from app.main.config.loader import (
    load_app_settings,
    load_keycloak_settings,
    load_logging_settings,
    load_s3_settings,
)
from app.main.config.settings import AppSettings, KeycloakSettings, S3Settings
from app.main.ioc.core import CoreProvider
from app.main.ioc.outbound import get_outbound_providers
from app.main.setup import setup_logging
from app.outbound.exceptions import ObjectNotFound


def create_service() -> FastAPI:
    logging_settings = load_logging_settings()

    setup_logging(level=logging_settings.LEVEL)

    app_settings = load_app_settings()
    s3_settings = load_s3_settings()
    keycloak_settings = load_keycloak_settings()
    app = FastAPI(
        debug=app_settings.DEBUG,
        title=app_settings.NAME,
        routes=[*make_stream_router().routes],
        exception_handlers={
            HTTPStatus.UNAUTHORIZED: JsendFailHandler(HTTPStatus.UNAUTHORIZED),
            HTTPStatus.FORBIDDEN: JsendFailHandler(HTTPStatus.FORBIDDEN),
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE: JsendFailHandler(HTTPStatus.UNSUPPORTED_MEDIA_TYPE),
            HTTPStatus.UNPROCESSABLE_CONTENT: JsendFailHandler(HTTPStatus.UNPROCESSABLE_CONTENT),
            HTTPStatus.NOT_FOUND: JsendFailHandler(HTTPStatus.NOT_FOUND),
            HTTPStatus.INTERNAL_SERVER_ERROR: JsendErrorHandler(HTTPStatus.INTERNAL_SERVER_ERROR),
            Unauthorized: JsendFailHandler(HTTPStatus.UNAUTHORIZED),
            Forbidden: JsendFailHandler(HTTPStatus.FORBIDDEN),
            NotFound: JsendFailHandler(HTTPStatus.NOT_FOUND),
            ObjectNotFound: JsendFailHandler(HTTPStatus.NOT_FOUND),
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
        CoreProvider(),
        FastapiProvider(),
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

    uvicorn.run(app=create_service(), host=app_settings.HOST, port=app_settings.PORT)

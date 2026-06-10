"""Module: Service application factory."""

from http import HTTPStatus

from fastapi import FastAPI

from management.common import handlers
from management.core import configs
from management.endpoints.v1 import uploads_router


def create_service() -> FastAPI:
    """Create a service."""
    # initialize service
    app = FastAPI(
        title=configs.ServiceConfig.name,
        exception_handlers={
            HTTPStatus.FORBIDDEN: handlers.forbidden_error_handler,
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE: handlers.unsupported_media_error_handler,
            HTTPStatus.UNPROCESSABLE_CONTENT: handlers.validation_error_handler,
            HTTPStatus.INTERNAL_SERVER_ERROR: handlers.internal_server_error_handler,
        },
        routes=[
            *uploads_router.routes
        ]
    )

    return app

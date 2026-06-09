"""Module: Service application factory."""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from management.common.handlers import validation_error_handler
from management.core import configs
from management.endpoints.v1 import uploads_router


def create_service() -> FastAPI:
    """Create a service."""
    app = FastAPI(
        title=configs.ServiceConfig.name,
    )
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.include_router(uploads_router)
    return app

"""Module: request validation exception handler."""

from http import HTTPStatus

from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from toolkit.service.response import ValidationErrorResponse


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle validation error."""
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
        content=ValidationErrorResponse(
            message=exc,
            data={"errors": exc.errors()},
        ).model_dump(),
    )

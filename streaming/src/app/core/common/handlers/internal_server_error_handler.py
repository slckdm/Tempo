"""Module: internal server error exception handler."""

from http import HTTPStatus

from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from toolkit.service.response import EmptyData, InternalServerErrorResponse


async def internal_server_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle internal server error."""
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=InternalServerErrorResponse(data=EmptyData()).model_dump(),
    )

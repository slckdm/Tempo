"""Module: forbidden request exception handler."""

from http import HTTPStatus

from fastapi.requests import Request
from fastapi.responses import JSONResponse

from toolkit.s3.s3_client import NoSuchKeyException
from toolkit.service.response import EmptyData, NotFoundResponse


async def no_such_key_error_handler(request: Request, exc: NoSuchKeyException) -> JSONResponse:
    """Handle forbidden error."""
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content=NotFoundResponse(data=EmptyData()).model_dump(),
    )

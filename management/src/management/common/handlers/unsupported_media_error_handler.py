"""Module: unsupported media request exception handler."""

from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from toolkit.service.response import UnsupportedMediaTypeResponse


async def unsupported_media_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle unsupported media error."""
    return JSONResponse(
        status_code=exc.status_code,
        content=UnsupportedMediaTypeResponse(
            message=exc.detail,
            data={},
        ).model_dump(),
    )

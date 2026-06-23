"""Module: unauthorized request exception handler."""

from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from toolkit.service.exceptions import TempoException
from toolkit.service.response import EmptyData, UnauthorizedResponse


async def unauthorized_error_handler(
    request: Request, exc: HTTPException | TempoException
) -> JSONResponse:
    """Handle unauthorized error."""
    return JSONResponse(
        status_code=exc.status_code,
        content=UnauthorizedResponse(message=exc.detail, data=EmptyData()).model_dump(),
    )

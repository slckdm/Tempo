"""Module: unauthorized request exception handler."""

from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from toolkit.service.response import UnauthorizedResponse


async def unauthorized_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle unauthorized error."""
    return JSONResponse(
        status_code=exc.status_code,
        content=UnauthorizedResponse(
            message=exc.detail,
            data={},
        ).model_dump(),
    )

"""Module: forbidden request exception handler."""

from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from toolkit.service.response import ForbiddenResponse


async def forbidden_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle forbidden error."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ForbiddenResponse(
            message=exc.detail,
            data={},
        ).model_dump(),
    )

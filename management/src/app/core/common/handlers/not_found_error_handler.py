"""Module: forbidden request exception handler."""

from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from toolkit.service.response import EmptyData, NotFoundResponse


async def not_found_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle forbidden error."""
    return JSONResponse(
        status_code=exc.status_code,
        content=NotFoundResponse(message=exc.detail, data=EmptyData()).model_dump(),
    )

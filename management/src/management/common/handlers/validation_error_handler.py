"""Module: request validation exception handler."""

from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from toolkit.response import JSendFailResponse


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=JSendFailResponse(
            code="JSEND-0002",
            message="Validation errors",
            data={"errors": exc.errors()},
        ).model_dump(),
    )

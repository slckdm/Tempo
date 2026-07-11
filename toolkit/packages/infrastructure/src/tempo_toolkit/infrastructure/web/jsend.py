"""JSend response models and FastAPI exception handlers."""

from enum import StrEnum
from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field


class EmptyData(BaseModel):
    """Empty response payload."""


class JSendStatus(StrEnum):
    """JSend response status."""

    SUCCESS = "success"
    FAIL = "fail"
    ERROR = "error"


class JSendResponse[DTO: BaseModel](BaseModel):
    """Base JSend response."""

    data: DTO = Field(default_factory=EmptyData, description="The data payload of the response.")


class JSendSuccessfulResponse[DTO: BaseModel](JSendResponse[DTO]):
    """Successful JSend response."""

    status: JSendStatus = Field(default=JSendStatus.SUCCESS)


class JSendFailResponse(JSendResponse):
    """Failed JSend response."""

    message: str
    status: JSendStatus = Field(default=JSendStatus.FAIL)


class JSendErrorResponse(JSendResponse):
    """Errored JSend response."""

    message: str
    status: JSendStatus = Field(default=JSendStatus.ERROR)


class BadRequestResponse(JSendFailResponse):
    """Bad-request response."""

    message: str = Field(default=HTTPStatus.BAD_REQUEST.phrase)


class ForbiddenResponse(JSendFailResponse):
    """Forbidden response."""

    message: str = Field(default=HTTPStatus.FORBIDDEN.phrase)


class InternalServerErrorResponse(JSendErrorResponse):
    """Internal-server-error response."""

    message: str = Field(default=HTTPStatus.INTERNAL_SERVER_ERROR.phrase)


class NotFoundResponse(JSendFailResponse):
    """Not-found response."""

    message: str = Field(default=HTTPStatus.NOT_FOUND.phrase)


class ValidationErrorResponse(JSendFailResponse):
    """Validation-error response."""

    message: str = Field(default=HTTPStatus.UNPROCESSABLE_CONTENT.phrase)


class UnsupportedMediaTypeResponse(JSendFailResponse):
    """Unsupported-media-type response."""

    message: str = Field(default=HTTPStatus.UNSUPPORTED_MEDIA_TYPE.phrase)


class UnauthorizedResponse(JSendFailResponse):
    """Unauthorized response."""

    message: str = Field(default=HTTPStatus.UNAUTHORIZED.phrase)


class ConflictResponse(JSendFailResponse):
    """Conflict response."""

    message: str = Field(default=HTTPStatus.CONFLICT.phrase)


class JSendErrorHandler:
    """Render an exception as a JSend error response."""

    def __init__(self, http_status: HTTPStatus) -> None:
        """Initialize the handler with its response status."""
        self._http_status = http_status

    async def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        """Render a JSend error response."""
        data: dict | EmptyData = getattr(exc, "data", None) or EmptyData()
        message: str = getattr(exc, "message", None) or self._http_status.phrase
        return JSONResponse(
            status_code=self._http_status,
            content=JSendErrorResponse(message=message, data=data).model_dump(),
        )


class JSendFailHandler:
    """Render an exception as a JSend fail response."""

    def __init__(self, http_status: HTTPStatus) -> None:
        """Initialize the handler with its response status."""
        self._http_status = http_status

    async def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        """Render a JSend fail response."""
        data: dict | EmptyData = getattr(exc, "data", None) or EmptyData()
        message: str = getattr(exc, "message", None) or self._http_status.phrase
        return JSONResponse(
            status_code=self._http_status,
            content=JSendFailResponse(message=message, data=data).model_dump(),
        )

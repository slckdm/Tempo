"""Module: JSend response."""

from enum import StrEnum
from http import HTTPStatus

from pydantic import BaseModel, Field


class EmptyData(BaseModel):
    """Empty data model."""


class JSendStatus(StrEnum):
    """JSend response status."""

    SUCCESS = "success"
    FAIL = "fail"
    ERROR = "error"


class JSendResponse[DTO: BaseModel](BaseModel):
    """JSend response base class."""

    data: DTO = Field(default_factory=EmptyData, description="The data payload of the response.")


class JSendSuccessfulResponse[DTO: BaseModel](JSendResponse[DTO]):
    """JSend successful response validation schema."""

    status: JSendStatus = Field(
        default=JSendStatus.SUCCESS, description="The status of the response"
    )


class JSendFailResponse(JSendResponse):
    """JSend fail response validation schema."""

    message: str = Field(description="A meaningful error message describing what went wrong.")
    status: JSendStatus = Field(
        default=JSendStatus.FAIL, description="The status of the response"
    )


class JSendErrorResponse(JSendResponse):
    """JSend error response validation schema."""

    message: str = Field(description="A meaningful error message describing what went wrong.")
    status: JSendStatus = Field(
        default=JSendStatus.ERROR, description="The status of the response"
    )


class BadRequestResponse(JSendFailResponse):
    """Bad request error response."""

    message: str = Field(default=HTTPStatus.BAD_REQUEST.phrase)


class ForbiddenResponse(JSendFailResponse):
    """Forbidden error response."""

    message: str = Field(default=HTTPStatus.FORBIDDEN.phrase)


class InternalServerErrorResponse(JSendErrorResponse):
    """Internal Server error response."""

    message: str = Field(default=HTTPStatus.INTERNAL_SERVER_ERROR.phrase)


class NotFoundResponse(JSendFailResponse):
    """Not found error response."""

    message: str = Field(default=HTTPStatus.NOT_FOUND.phrase)


class ValidationErrorResponse(JSendFailResponse):
    """Validation error response."""

    message: str = Field(default=HTTPStatus.UNPROCESSABLE_CONTENT.phrase)


class UnsupportedMediaTypeResponse(JSendFailResponse):
    """Unsupported media type error response."""

    message: str = Field(default=HTTPStatus.UNSUPPORTED_MEDIA_TYPE.phrase)


class UnauthorizedResponse(JSendFailResponse):
    """Unauthorized error response."""

    message: str = Field(default=HTTPStatus.UNAUTHORIZED.phrase)

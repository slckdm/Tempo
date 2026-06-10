"""Module: Internal Server Error Error Response Model."""

from http import HTTPStatus

from pydantic import Field

from .response import JSendErrorResponse


class InternalServerErrorResponse(JSendErrorResponse):
    """Internal Server error response."""

    message: str = Field(default=HTTPStatus.INTERNAL_SERVER_ERROR.phrase)

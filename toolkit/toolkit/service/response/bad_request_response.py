"""Module: Bad Request Error Response Model."""

from http import HTTPStatus

from pydantic import Field

from .response import JSendFailResponse


class BadRequestResponse(JSendFailResponse):
    """Bad request error response."""

    message: str = Field(default=HTTPStatus.BAD_REQUEST.phrase)

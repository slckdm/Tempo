"""Module: Not Found Error Response Model."""

from http import HTTPStatus

from pydantic import Field

from .response import JSendFailResponse


class NotFoundResponse(JSendFailResponse):
    """Not found error response."""

    message: str = Field(default=HTTPStatus.NOT_FOUND.phrase)

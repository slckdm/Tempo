"""Module: Unauthorized Error Response Model."""

from http import HTTPStatus

from pydantic import Field

from .response import JSendFailResponse


class UnauthorizedResponse(JSendFailResponse):
    """Unauthorized error response."""

    message: str = Field(default=HTTPStatus.UNAUTHORIZED.phrase)

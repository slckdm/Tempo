"""Module: Forbidden Error Response Model."""

from http import HTTPStatus

from pydantic import Field

from .response import JSendFailResponse


class ForbiddenResponse(JSendFailResponse):
    """Forbidden error response."""

    message: str = Field(default=HTTPStatus.FORBIDDEN.phrase)

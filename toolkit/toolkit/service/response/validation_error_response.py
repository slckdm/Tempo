"""Module: Validation Error Response Model."""

from http import HTTPStatus

from pydantic import Field

from .response import JSendFailResponse


class ValidationErrorResponse(JSendFailResponse):
    """Validation error response."""

    message: str = Field(default=HTTPStatus.UNPROCESSABLE_CONTENT.phrase)

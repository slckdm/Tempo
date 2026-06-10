"""Module: Unsupported Media Type Error Response Model."""

from http import HTTPStatus

from pydantic import Field

from .response import JSendFailResponse


class UnsupportedMediaTypeResponse(JSendFailResponse):
    """Unsupported media type error response."""

    message: str = Field(default=HTTPStatus.UNSUPPORTED_MEDIA_TYPE.phrase)

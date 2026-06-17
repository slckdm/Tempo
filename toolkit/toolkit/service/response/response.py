"""Module: JSend response."""

from enum import StrEnum
from typing import Annotated

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

    data: Annotated[
        DTO,
        Field(default=EmptyData(), description="The data payload of the response.")
    ]


class JSendSuccessfulResponse[DTO: BaseModel](JSendResponse[DTO]):
    """JSend successful response validation schema."""

    status: JSendStatus = Field(
        default=JSendStatus.SUCCESS, description="The status of the response"
    )


class JSendFailResponse(JSendResponse):
    """JSend fail response validation schema."""

    status: JSendStatus = Field(default=JSendStatus.FAIL, description="The status of the response")
    message: str = Field(description="A meaningful error message describing what went wrong.")


class JSendErrorResponse(JSendResponse):
    """JSend error response validation schema."""

    status: JSendStatus = Field(
        default=JSendStatus.ERROR, description="The status of the response"
    )
    message: str = Field(description="A meaningful error message describing what went wrong.")

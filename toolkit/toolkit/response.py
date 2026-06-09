from typing import Optional

from pydantic import BaseModel, Field
from enum import StrEnum


class JSendStatus(StrEnum):
    SUCCESS = "success"
    FAIL = "fail"
    ERROR = "error"


class DTO(BaseModel):
    ...


class JSendResponse[DTO](BaseModel):
    data: DTO = Field(description="The data payload of the successful response.")


class JSendSuccessfulResponse[DTO](JSendResponse[DTO]):
    status: Optional[JSendStatus] = Field(default=JSendStatus.SUCCESS, description="The status of the response")


class JSendFailResponse(JSendResponse):
    status: JSendStatus = Field(default=JSendStatus.FAIL, description="The status of the response")
    message: str = Field(description="A meaningful error message describing what went wrong.")
    code: str = Field(description="An optional error code that can be used to identify the type of failure.")


class JSendErrorResponse(JSendResponse):
    status: JSendStatus = Field(default=JSendStatus.ERROR, description="The status of the response")
    message: str = Field(description="A meaningful error message describing what went wrong.")
    code: str = Field(description="An optional error code that can be used to identify the type of error.")

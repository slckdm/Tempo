"""Module: validation schema for create upload request body."""

from pydantic import BaseModel, Field

from ..dto import UploadDTO


class CreateUploadResponseBody(BaseModel):
    """Create upload response body DTO."""

    upload: UploadDTO = Field(description="Upload data")
    presigned_url: str = Field(
        description="Presigned URL for uploading",
        json_schema_extra={"example": "http://some.url/here/bla-bla-bla"},
    )

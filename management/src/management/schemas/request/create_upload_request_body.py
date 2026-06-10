"""Module: create upload request body schema."""

from pydantic import BaseModel, Field


class CreateUploadRequestBody(BaseModel):
    """Create upload request body schema."""

    filename: str
    content_type: str = Field(alias="contentType")
    size: int

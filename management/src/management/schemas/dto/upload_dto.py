"""Module: Upload DTO."""

from pydantic import BaseModel, Field


class UploadDTO(BaseModel):
    """Upload Data Transfer Object."""

    urn: str = Field(
        description="The URN of the upload.",
        json_schema_extra={"example": "urn:management.upload:123"}
    )

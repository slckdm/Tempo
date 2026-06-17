"""Module: Upload DTO."""

from pydantic import BaseModel

from app.core.common.types_ import UploadURNType


class UploadDTO(BaseModel):
    """Upload Data Transfer Object."""

    urn: UploadURNType

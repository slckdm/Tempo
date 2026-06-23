"""Module: Upload DTO."""

from pydantic import BaseModel

from toolkit.types.urn import UploadURNType


class UploadDTO(BaseModel):
    """Upload Data Transfer Object."""

    urn: UploadURNType

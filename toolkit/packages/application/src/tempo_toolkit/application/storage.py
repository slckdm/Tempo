"""Object-storage model and port."""

from io import IOBase
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field, SkipValidation


class StoredObject(BaseModel):
    """Object returned by object storage."""

    body: SkipValidation[IOBase] = Field(alias="Body")
    content_range: str | None = Field(None, alias="ContentRange")
    content_length: int = Field(alias="ContentLength")
    content_type: str = Field(alias="ContentType")

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)


class ObjectStorage(Protocol):
    """Object-storage operations used by applications."""

    async def get_object(self, key: str, **kwargs: object) -> StoredObject:
        """Get an object."""
        ...

    async def put_object(self, key: str, body: bytes, **kwargs: object) -> None:
        """Store an object."""
        ...

    async def make_object_upload_url(
        self, key: str, content_type: str, content_length: int
    ) -> str:
        """Create a presigned upload URL."""
        ...

    async def delete_object(self, key: str, **kwargs: object) -> None:
        """Delete an object."""
        ...

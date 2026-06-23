from datetime import datetime
from uuid import UUID

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from toolkit.types.enum import UploadStatus
from toolkit.types.urn import UploadURNType

faker = Faker()


class TrackMetadataDTO(BaseModel):
    upload_id: UploadURNType = Field(alias="urn")
    title: str | None = Field(
        None,
    )
    artist: str | None = Field(None, json_schema_extra={"example": faker.name()})
    album: str | None = Field(None, json_schema_extra={"example": faker.name()})
    albumartist: str | None = Field(None, json_schema_extra={"example": faker.name()})
    genre: str | None = Field(None, json_schema_extra={"example": faker.word()})
    year: str | None = Field(None, json_schema_extra={"example": faker.year()})
    track_number: int | None = Field(None, json_schema_extra={"example": faker.random_digit()})
    disc: int | None = Field(None, json_schema_extra={"example": faker.random_digit()})
    duration: float | None = Field(
        None, json_schema_extra={"example": float(faker.random_digit())}
    )
    bitrate: float | None = Field(None, json_schema_extra={"example": float(faker.random_digit())})
    samplerate: int | None = Field(None, json_schema_extra={"example": faker.random_digit()})
    channels: int | None = Field(None, json_schema_extra={"example": faker.random_digit()})
    comment: str | None = Field(None, json_schema_extra={"example": faker.text()})
    cover_key: str | None = Field(None, json_schema_extra={"example": "some/string"})
    filename: str = Field(json_schema_extra={"example": faker.file_name(category="audio")})
    content_type: str = Field(json_schema_extra={"example": faker.mime_type("audio")})
    size: int = Field(json_schema_extra={"example": faker.random_digit()})
    created_by: UUID = Field(json_schema_extra={"example": faker.uuid1()})
    created_at: datetime = Field(json_schema_extra={"example": faker.date()})
    updated_at: datetime = Field(json_schema_extra={"example": faker.date()})
    processing_status: UploadStatus = Field(json_schema_extra={"example": UploadStatus.COMPLETED})
    origin_upload_status: UploadStatus = Field(
        json_schema_extra={"example": UploadStatus.COMPLETED}
    )
    error: str | None = Field(None, json_schema_extra={"example": faker.text()})

    model_config = ConfigDict(from_attributes=True)

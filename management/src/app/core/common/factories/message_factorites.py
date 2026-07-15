from tempo_toolkit.contracts.events import (
    UploadCompletedEvent,
    UploadCreatedEvent,
    UploadDeletedEvent,
)

from app.core.models.upload import Upload


def make_upload_completed_message(upload: Upload) -> UploadCompletedEvent:
    return UploadCompletedEvent(
        upload_id=upload.urn,
        s3_key=str(upload.urn),
        filename=upload.filename,
        content_type=upload.content_type,
        size=upload.size,
        created_by=upload.created_by,
        created_at=upload.created_at,
        status=upload.status,
    )


def make_upload_created_message(upload: Upload) -> UploadCreatedEvent:
    return UploadCreatedEvent(
        upload_id=upload.urn,
        s3_key=str(upload.urn),
        filename=upload.filename,
        content_type=upload.content_type,
        size=upload.size,
        created_by=upload.created_by,
        created_at=upload.created_at,
        status=upload.status,
    )


def make_upload_deleted_message(upload: Upload) -> UploadDeletedEvent:
    return UploadDeletedEvent(upload_id=upload.urn, s3_key=str(upload.urn))

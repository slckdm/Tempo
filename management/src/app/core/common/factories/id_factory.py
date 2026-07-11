from uuid import uuid4

from app.core.common.types import UploadID


def generate_upload_id() -> UploadID:
    return UploadID(uuid4())

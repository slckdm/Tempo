from enum import StrEnum

from app.core.common.types_ import UploadURNType


class EventType(StrEnum):
    UPLOAD_CREATED = f"event:{UploadURNType.namespace}:created"
    UPLOAD_COMPLETED = f"event:{UploadURNType.namespace}:completed"

from uuid import UUID

from toolkit.types_ import URNType


class UploadURNType(URNType[UUID]):
    """Upload URN type."""

    namespace = "mng.upload"

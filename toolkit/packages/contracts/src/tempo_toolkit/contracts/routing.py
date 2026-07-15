"""Stable message routing keys."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RoutingKey:
    """RabbitMQ routing key value."""

    route: str
    prefix: str = "rk"

    def __str__(self) -> str:
        """Return the broker routing-key value."""
        return f"{self.prefix}.{self.route}"


UPLOAD_CREATED_RK = RoutingKey("tempo.mng.upload.created")
UPLOAD_COMPLETED_RK = RoutingKey("tempo.mng.upload.completed")
UPLOAD_DELETED_RK = RoutingKey("tempo.mng.upload.deleted")
METADATA_READY_RK = RoutingKey("tempo.md.metadata.ready")
METADATA_FAILED_RK = RoutingKey("tempo.md.metadata.failed")
METADATA_DELETED_RK = RoutingKey("tempo.md.metadata.deleted")
# Commands RK
# - Metadata
METADATA_PROCESS_METADATA_RK = RoutingKey("tempo.md.metadata.process_metadata")
METADATA_DELETE_METADATA_RK = RoutingKey("tempo.md.metadata.delete_metadata")

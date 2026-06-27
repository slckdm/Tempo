from dataclasses import dataclass


@dataclass(frozen=True, unsafe_hash=True)
class RoutingKey:
    route: str
    prefix: str = "rk"

    def __str__(self) -> str:
        return f"{self.prefix}.{self.route}"


# Routing keys
UPLOAD_CREATED_RK = RoutingKey("tempo.mng.upload.created")
UPLOAD_COMPLETED_RK = RoutingKey("tempo.mng.upload.completed")
METADATA_READY_RK = RoutingKey("tempo.md.metadata.ready")
METADATA_FAILED_RK = RoutingKey("tempo.md.metadata.failed")

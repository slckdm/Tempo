from app.core.models.qdrant.track_features_collection import make_track_features_collection
from app.outbound.qdrant.registry import CollectionsRegistry


def register_collections() -> None:
    """Register all collections in the application."""
    CollectionsRegistry.register(make_track_features_collection())

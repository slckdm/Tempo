from qdrant_client.http.models import Distance, VectorParams

from app.core.common.enums.collections import Collections
from app.core.models.qdrant.collection_base import Collection


def make_track_features_collection() -> Collection:
    return Collection(
        name=Collections.TRACK_FEATURES,
        vectors_config=VectorParams(size=34, distance=Distance.COSINE),
    )

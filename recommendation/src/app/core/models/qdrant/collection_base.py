
from dataclasses import dataclass

from qdrant_client.http.models import VectorParams


@dataclass(frozen=True, kw_only=True)
class Collection:
    name: str
    vectors_config: VectorParams

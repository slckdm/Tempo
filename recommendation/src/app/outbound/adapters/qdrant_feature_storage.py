from qdrant_client import AsyncQdrantClient
from qdrant_client.conversions.common_types import PointStruct

from app.core.commands.ports.feature_storage import FeatureStorage
from app.core.common.entities.collection_metadata import CollectionMetadata


class QdrantFeatureStorage(FeatureStorage):
    def __init__(self, qdrant_client: AsyncQdrantClient) -> None:
        self._qdrant_client = qdrant_client

    async def save(
        self,
        collection: str,
        id: str,
        vector: list[int | float],
        metadata: CollectionMetadata,
    ) -> None:
        await self._qdrant_client.upsert(
            collection, points=[PointStruct(id=id, vector=vector, payload=metadata.to_dict())]
        )

    async def delete(self, collection: str, *id: str) -> None:
        await self._qdrant_client.delete(
            collection_name=collection,
            points_selector=list(id),
        )

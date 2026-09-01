
from typing import Iterator

from app.core.models.qdrant.collection_base import Collection


class CollectionsRegistry:

    __instances: dict[str, Collection] = {}

    @classmethod
    def register(cls, /, *_collection: Collection) -> None:
        for collection in _collection:
            cls.__instances[collection.name] = collection

    @classmethod
    def get_collection(cls, collection_name: str) -> Collection | None:
        return cls.__instances.get(collection_name)

    @classmethod
    def collections(cls) -> Iterator[Collection]:
        return iter(cls.__instances.values())

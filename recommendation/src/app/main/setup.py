import logging

from qdrant_client import QdrantClient

from tempo_toolkit.infrastructure.logging import DATEFMT, FMT, LoggingLevel

from app.main.config.settings import QdrantSettings
from app.outbound.qdrant.registry import CollectionsRegistry

logger = logging.getLogger(__name__)


def setup_logging(*, level: LoggingLevel = LoggingLevel.INFO) -> None:
    logging.basicConfig(level=level, datefmt=DATEFMT, format=FMT, force=True)
    logger.info("Logging is set up")


def setup_qdrant_collections(config: QdrantSettings) -> None:
    qdrant_client = QdrantClient(host=config.HOST, port=config.PORT)

    for collection in CollectionsRegistry.collections():
        if not qdrant_client.collection_exists(collection.name):
            qdrant_client.create_collection(
                collection_name=collection.name,
                vectors_config=collection.vectors_config,
            )

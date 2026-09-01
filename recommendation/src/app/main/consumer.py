import asyncio
import logging

from dishka import make_async_container
from dishka_faststream import FastStreamProvider, setup_dishka
from faststream import FastStream

from tempo_toolkit.infrastructure.cache import RedisClientProvider, RedisSettings
from tempo_toolkit.infrastructure.database import PostgresProvider, PostgresSettings
from tempo_toolkit.infrastructure.identity import KeycloakSettings
from tempo_toolkit.infrastructure.messaging import (
    RECOMMENDATIONS_DLE,
    RECOMMENDATIONS_DLQ,
    make_rabbit_broker,
)
from tempo_toolkit.infrastructure.object_storage import S3Provider, S3Settings

from app.inbound.amqp.v1_router import make_v1_router
from app.main.config.loader import (
    load_keycloak_settings,
    load_logging_settings,
    load_postgres_settings,
    load_qdrant_settings,
    load_rabbitmq_settings,
    load_redis_settings,
    load_s3_settings,
)
from app.main.config.settings import QdrantSettings
from app.main.ioc.consumer import ConsumerProvider
from app.main.ioc.outbound import OutboxProvider, QdrantClientProvider
from app.main.setup import setup_logging, setup_qdrant_collections
from app.outbound.qdrant.all import register_collections
from app.outbound.sqlalchemy.mappings.all import map_tables


async def create_app() -> None:
    logging_settings = load_logging_settings()
    qdrant_settings = load_qdrant_settings()
    setup_logging(level=logging_settings.LEVEL)
    map_tables()
    register_collections()
    setup_qdrant_collections(config=qdrant_settings)
    rmq_settings = load_rabbitmq_settings()

    broker = make_rabbit_broker(rmq_settings)
    await broker.connect()
    broker.include_router(make_v1_router())
    await broker.declare_exchange(RECOMMENDATIONS_DLE)
    await broker.declare_queue(RECOMMENDATIONS_DLQ)

    app = FastStream(broker)

    container = make_async_container(
        FastStreamProvider(),
        ConsumerProvider(),
        RedisClientProvider(),
        PostgresProvider(),
        OutboxProvider(),
        QdrantClientProvider(),
        S3Provider(),
        context={
            PostgresSettings: load_postgres_settings(),
            RedisSettings: load_redis_settings(),
            S3Settings: load_s3_settings(),
            KeycloakSettings: load_keycloak_settings(),
            QdrantSettings: qdrant_settings,
        },
    )

    setup_dishka(container, app)

    logging.info("Starting consumer service")
    await app.run()


if __name__ == "__main__":
    asyncio.run(create_app())

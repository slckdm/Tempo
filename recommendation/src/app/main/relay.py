import asyncio
import logging

from dishka import make_async_container
from faststream.rabbit import RabbitBroker, RabbitExchange

from tempo_toolkit.infrastructure.database import PostgresProvider, PostgresSettings
from tempo_toolkit.infrastructure.identity import KeycloakSettings
from tempo_toolkit.infrastructure.messaging import (
    METADATA_EXCHANGE,
    make_rabbit_broker,
)
from tempo_toolkit.infrastructure.object_storage import S3Provider, S3Settings

from app.core.commands.publish_outbox_messages import PublishOutboxMessages
from app.main.config.loader import (
    load_keycloak_settings,
    load_logging_settings,
    load_postgres_settings,
    load_rabbitmq_settings,
    load_s3_settings,
)
from app.main.ioc.outbound import KeycloakClientProvider, OutboxProvider
from app.main.ioc.relay import RelayProvider
from app.main.setup import setup_logging
from app.outbound.sqlalchemy.mappings.all import map_tables


async def start_relay() -> None:
    logging_settings = load_logging_settings()

    setup_logging(level=logging_settings.LEVEL)
    map_tables()

    rmq_settings = load_rabbitmq_settings()

    broker = make_rabbit_broker(rmq_settings)
    await broker.connect()
    await broker.declare_exchange(METADATA_EXCHANGE)

    container = make_async_container(
        RelayProvider(),
        KeycloakClientProvider(),
        PostgresProvider(),
        S3Provider(),
        OutboxProvider(),
        context={
            PostgresSettings: load_postgres_settings(),
            RabbitBroker: broker,
            KeycloakSettings: load_keycloak_settings(),
            S3Settings: load_s3_settings(),
            RabbitExchange: METADATA_EXCHANGE
        },
    )

    logging.info("Starting publisher service")
    try:
        while True:
            async with container() as scope:
                relay = await scope.get(PublishOutboxMessages)
                await relay()
            await asyncio.sleep(1)
    finally:
        await broker.stop()
        await container.close()


if __name__ == "__main__":
    asyncio.run(start_relay())

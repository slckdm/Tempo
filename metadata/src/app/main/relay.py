import asyncio
import logging

from dishka import make_async_container
from faststream.rabbit import RabbitBroker

from toolkit.messaging.broker import (
    METADATA_DLE,
    METADATA_DLQ,
    METADATA_EXCHANGE,
    make_rabbit_broker,
)

from app.core.commands.publish_outbox_messages import PublishOutboxMessages
from app.main.config.loader import (
    load_keycloak_settings,
    load_logging_settings,
    load_postgres_settings,
    load_rabbitmq_settings,
    load_s3_settings,
)
from app.main.config.settings import KeycloakSettings, PostgresSettings, S3Settings
from app.main.ioc.outbound import get_outbound_providers
from app.main.ioc.relay import RelayProvider
from app.main.setup import setup_logging


async def start_relay() -> None:
    logging_settings = load_logging_settings()
    setup_logging(level=logging_settings.LEVEL)

    rmq_settings = load_rabbitmq_settings()

    broker = make_rabbit_broker(rmq_settings)
    await broker.connect()
    await broker.declare_exchange(METADATA_EXCHANGE)
    await broker.declare_exchange(METADATA_DLE)
    await broker.declare_queue(METADATA_DLQ)

    container = make_async_container(
        RelayProvider(),
        *get_outbound_providers(),
        context={
            PostgresSettings: load_postgres_settings(),
            RabbitBroker: broker,
            KeycloakSettings: load_keycloak_settings(),
            S3Settings: load_s3_settings(),
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

from typing import TYPE_CHECKING

from faststream.rabbit import ExchangeType, QueueType, RabbitBroker, RabbitExchange, RabbitQueue
from faststream.security import SASLPlaintext

from .settings import RabbitMQSettings

if TYPE_CHECKING:
    from .routing import RoutingKey


def make_rabbit_broker(settings: RabbitMQSettings) -> RabbitBroker:
    rabbit_broker = RabbitBroker(
        host=settings.HOST,
        port=settings.PORT,
        virtualhost=settings.VHOST,
        app_id=settings.APP_ID,
        security=SASLPlaintext(username=settings.USER, password=settings.PASSWORD),
    )

    return rabbit_broker


def make_queue(
    name: str,
    routing_key: RoutingKey,
    dlx: RabbitExchange,
    queue_type: QueueType = QueueType.QUORUM,
    durable: bool = True,
) -> RabbitQueue:
    args = {
        "x-delivery-limit": 3,
        "x-dead-letter-exchange": dlx.name,
    }
    return RabbitQueue(
        name,
        queue_type=queue_type,
        durable=durable,
        routing_key=str(routing_key),
        arguments=args,
    )


_MANAGEMENT_NAMESPACE = "tempo.management"
_METADATA_NAMESPACE = "tempo.metadata"
_LIBRARY_NAMESPACE = "tempo.library"

# Exchanges
MANAGEMENT_EXCHANGE = RabbitExchange(f"{_MANAGEMENT_NAMESPACE}.exchange", ExchangeType.TOPIC)
METADATA_EXCHANGE = RabbitExchange(f"{_METADATA_NAMESPACE}.exchange", ExchangeType.TOPIC)
LIBRARY_EXCHANGE = RabbitExchange(f"{_LIBRARY_NAMESPACE}.exchange", ExchangeType.TOPIC)
MANAGEMENT_DLE = RabbitExchange(f"{_MANAGEMENT_NAMESPACE}.dle", ExchangeType.FANOUT)
METADATA_DLE = RabbitExchange(f"{_METADATA_NAMESPACE}.dle", ExchangeType.FANOUT)
LIBRARY_DLE = RabbitExchange(f"{_LIBRARY_NAMESPACE}.dle", ExchangeType.FANOUT)

# queues
MANAGEMENT_DLQ = RabbitQueue(f"{_MANAGEMENT_NAMESPACE}.dlq", durable=True)
METADATA_DLQ = RabbitQueue(f"{_METADATA_NAMESPACE}.dlq", durable=True)
LIBRARY_DLQ = RabbitQueue(f"{_LIBRARY_NAMESPACE}.dlq", durable=True)

MANAGEMENT_CONSUMER_QUEUE = RabbitQueue(f"{_MANAGEMENT_NAMESPACE}.queue", durable=True)
METADATA_CONSUMER_QUEUE = RabbitQueue(f"{_METADATA_NAMESPACE}.queue", durable=True)
LIBRARY_CONSUMER_QUEUE = RabbitQueue(f"{_LIBRARY_NAMESPACE}.queue", durable=True)

from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange, RabbitQueue, QueueType
from faststream.security import SASLPlaintext

from .settings import RabbitMQSettings


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
    routing_key: str,
    dlx: RabbitExchange,
    queue_type: QueueType = QueueType.QUORUM,
    durable: bool = True,
) -> RabbitQueue:
    args = {
        "x-delivery-limit": 3,
        "x-dead-letter-exchange": dlx.name,
    }
    return RabbitQueue(routing_key, queue_type=queue_type, durable=durable, arguments=args)


_MANAGEMENT_NAMESPACE = "tempo.management"
_METADATA_NAMESPACE = "tempo.metadata"

# Exchanges
MANAGEMENT_EXCHANGE = RabbitExchange(f"{_MANAGEMENT_NAMESPACE}.exchange", ExchangeType.TOPIC)
METADATA_EXCHANGE = RabbitExchange(f"{_METADATA_NAMESPACE}.exchange", ExchangeType.TOPIC)
MANAGEMENT_DLE = RabbitExchange(f"{_MANAGEMENT_NAMESPACE}.dle", ExchangeType.FANOUT)
METADATA_DLE = RabbitExchange(f"{_METADATA_NAMESPACE}.dle", ExchangeType.FANOUT)

# queues
MANAGEMENT_DLQ = RabbitQueue(f"{_MANAGEMENT_NAMESPACE}.dlq", durable=True)
METADATA_DLQ = RabbitQueue(f"{_METADATA_NAMESPACE}.dlq", durable=True)

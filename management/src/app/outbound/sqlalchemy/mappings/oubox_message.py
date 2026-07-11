
from tempo_toolkit.application.outbox import OutboxMessage
from tempo_toolkit.infrastructure.database import make_outbox_message_table

from app.outbound.sqlalchemy.registry import mapper_registry

outbox_messages_table = make_outbox_message_table(mapper_registry)


def map_outbox_table() -> None:
    mapper_registry.map_imperatively(
        OutboxMessage,
        outbox_messages_table
    )

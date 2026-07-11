from typing import NewType

from sqlalchemy import JSON, UUID, Column, DateTime, Index, String, Table, orm, text

OutboxTable = NewType("OutboxTable", Table)


def make_outbox_message_table(registry: orm.registry) -> OutboxTable:
    return Table(
        "outbox_messages",
        registry.metadata,
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column("aggregate_type", String, nullable=False),
        Column("aggregate_id", UUID, nullable=False),
        Column("event_type", String, nullable=False),
        Column("payload", JSON, nullable=False),
        Column("created_at", DateTime(timezone=True), nullable=False),
        Column("published_at", DateTime(timezone=True), nullable=True),
        Index(
            "ix_outbox_messages_unpublished_id",
            "id",
            postgresql_where=text("published_at IS NULL"),
        ),
    )

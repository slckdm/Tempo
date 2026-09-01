from app.outbound.sqlalchemy.mappings.outbox_message import map_outbox_table
from app.outbound.sqlalchemy.registry import mapper_registry


def map_tables() -> None:
    if mapper_registry.mappers:
        return
    map_outbox_table()

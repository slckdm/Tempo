from app.outbound.sqlalchemy.mappings.oubox_message import map_outbox_table
from app.outbound.sqlalchemy.mappings.upload import map_uploads_table
from app.outbound.sqlalchemy.registry import mapper_registry


def map_tables() -> None:
    if mapper_registry.mappers:
        return
    map_outbox_table()
    map_uploads_table()

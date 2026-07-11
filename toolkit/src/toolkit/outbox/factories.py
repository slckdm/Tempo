from uuid import uuid4

from toolkit.outbox.types import OutboxMessageID


def generate_outbox_message_id() -> OutboxMessageID:
    return OutboxMessageID(uuid4())

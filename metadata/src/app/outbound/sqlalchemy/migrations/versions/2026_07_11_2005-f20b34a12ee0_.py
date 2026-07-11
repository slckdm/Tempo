"""Convert outbox message IDs to UUID.

Revision ID: f20b34a12ee0
Revises: 76729e0db655
Create Date: 2026-07-11 20:05:47.836443

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f20b34a12ee0"
down_revision: Union[str, Sequence[str], None] = "76729e0db655"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE outbox_messages ALTER COLUMN id DROP DEFAULT")
    op.alter_column(
        "outbox_messages",
        "id",
        existing_type=sa.INTEGER(),
        type_=sa.UUID(),
        existing_nullable=False,
        postgresql_using="lpad(to_hex(id), 32, '0')::uuid",
    )
    op.execute("DROP SEQUENCE IF EXISTS outbox_messages_id_seq")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("CREATE SEQUENCE outbox_messages_id_seq")
    op.alter_column(
        "outbox_messages",
        "id",
        existing_type=sa.UUID(),
        type_=sa.INTEGER(),
        existing_nullable=False,
        postgresql_using=("nextval('outbox_messages_id_seq'::regclass)::integer"),
    )
    op.execute("ALTER SEQUENCE outbox_messages_id_seq OWNED BY outbox_messages.id")
    op.alter_column(
        "outbox_messages",
        "id",
        existing_type=sa.INTEGER(),
        existing_nullable=False,
        server_default=sa.text("nextval('outbox_messages_id_seq'::regclass)"),
    )

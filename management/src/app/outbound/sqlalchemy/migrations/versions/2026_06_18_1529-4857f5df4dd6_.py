"""Add 'PROCESSING' value for uploadstatus enum.

Revision ID: 4857f5df4dd6
Revises: aeac8404c10c
Create Date: 2026-06-18 15:29:09.770117

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4857f5df4dd6"
down_revision: Union[str, Sequence[str], None] = "aeac8404c10c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "aeac8404c10c"


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE uploadstatus ADD VALUE IF NOT EXISTS 'PROCESSING'")


def downgrade() -> None:
    """Downgrade schema."""
    pass

"""Add favorite user track unique constraint.

Revision ID: 6f7c8d9e0a1b
Revises: 2cdf38ea63ea
Create Date: 2026-07-10 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6f7c8d9e0a1b"
down_revision: Union[str, Sequence[str], None] = "2cdf38ea63ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = "2cdf38ea63ea"


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uq_favorites_user_id_track_id",
        "favorites",
        ["user_id", "track_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_favorites_user_id_track_id",
        "favorites",
        type_="unique",
    )

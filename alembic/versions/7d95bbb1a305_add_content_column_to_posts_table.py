"""add content column to posts table

Revision ID: 7d95bbb1a305
Revises: f4be258e0a77
Create Date: 2025-08-28 14:54:06.195167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d95bbb1a305'
down_revision: Union[str, Sequence[str], None] = 'f4be258e0a77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts","content")
    pass

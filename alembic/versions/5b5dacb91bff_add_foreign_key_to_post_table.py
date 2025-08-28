"""add foreign key to post table

Revision ID: 5b5dacb91bff
Revises: f557a1cc8a52
Create Date: 2025-08-28 15:42:02.862110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b5dacb91bff'
down_revision: Union[str, Sequence[str], None] = 'f557a1cc8a52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users",
                           local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE" )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_users_fk", table_name="posts") 
    op.drop_column("posts","owner_id")
    pass

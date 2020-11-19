"""empty message
# flake8: noqa
Revision ID: 773a734e8e5c
Revises: 
Create Date: 2020-11-17 02:05:09.741918
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "773a734e8e5c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "table_01",
        sa.Column("id", sa.SmallInteger(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    pass

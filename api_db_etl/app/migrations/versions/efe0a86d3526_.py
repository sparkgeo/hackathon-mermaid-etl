"""empty message
# flake8: noqa
Revision ID: efe0a86d3526
Revises: 8620afe56960
Create Date: 2020-11-19 00:00:14.110682
"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "efe0a86d3526"
down_revision = "8620afe56960"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("site", "_source_id")


def downgrade():
    op.add_column(
        "site",
        sa.Column("_source_id", postgresql.UUID(), autoincrement=False, nullable=False),
    )

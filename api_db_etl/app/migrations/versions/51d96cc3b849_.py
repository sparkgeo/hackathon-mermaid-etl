"""empty message
# flake8: noqa
Revision ID: 51d96cc3b849
Revises: a88d76167dc0
Create Date: 2020-11-17 23:24:22.665624
"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "51d96cc3b849"
down_revision = "a88d76167dc0"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("site", sa.Column("_source_id", postgresql.UUID(), nullable=False))
    op.drop_index("idx_site_location", table_name="site")


def downgrade():
    op.create_index("idx_site_location", "site", ["location"], unique=False)
    op.drop_column("site", "_source_id")

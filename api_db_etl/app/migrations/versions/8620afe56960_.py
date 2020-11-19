"""empty message
# flake8: noqa
Revision ID: 8620afe56960
Revises: d577f6443ce5
Create Date: 2020-11-18 22:56:25.223791
"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision = "8620afe56960"
down_revision = "d577f6443ce5"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION if not exists pg_trgm;")


def downgrade():
    op.execute("DROP EXTENSION pg_trgm;")

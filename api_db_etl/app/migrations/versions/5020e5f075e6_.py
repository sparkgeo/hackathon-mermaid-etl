"""empty message
# flake8: noqa
Revision ID: 5020e5f075e6
Revises: 51d96cc3b849
Create Date: 2020-11-17 23:48:46.340072
"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5020e5f075e6"
down_revision = "51d96cc3b849"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "site", "predecessor_id", existing_type=postgresql.UUID(), nullable=True
    )


def downgrade():
    op.alter_column(
        "site", "predecessor_id", existing_type=postgresql.UUID(), nullable=False
    )

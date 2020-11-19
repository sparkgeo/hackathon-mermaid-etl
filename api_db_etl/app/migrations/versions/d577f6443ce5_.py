"""empty message
# flake8: noqa
Revision ID: d577f6443ce5
Revises: e166f82899ad
Create Date: 2020-11-18 17:49:24.189375
"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "d577f6443ce5"
down_revision = "e166f82899ad"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "site",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("_source_id", postgresql.UUID(), nullable=False),
        sa.Column(
            "created_on",
            sa.DateTime(),
            server_default=sa.text("(now() at time zone 'utc')"),
            nullable=False,
        ),
        sa.Column(
            "updated_on",
            sa.DateTime(),
            server_default=sa.text("(now() at time zone 'utc')"),
            nullable=False,
        ),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "location",
            geoalchemy2.types.Geography(
                geometry_type="POINT", from_text="ST_GeogFromText", name="geography"
            ),
            nullable=False,
        ),
        sa.Column("notes", sa.Text(), nullable=False),
        sa.Column("country_id", postgresql.UUID(), nullable=False),
        sa.Column("exposure_id", postgresql.UUID(), nullable=False),
        sa.Column("project_id", postgresql.UUID(), nullable=False),
        sa.Column("reef_type_id", postgresql.UUID(), nullable=False),
        sa.Column("reef_zone_id", postgresql.UUID(), nullable=False),
        sa.Column("updated_by_id", postgresql.UUID(), nullable=False),
        sa.Column("predecessor_id", postgresql.UUID(), nullable=True),
        sa.Column(
            "validations", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("created_by_id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"], ["project.id"], name="site_project_id_ref_constraint"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("site")

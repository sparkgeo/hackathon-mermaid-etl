"""empty message
# flake8: noqa
Revision ID: e166f82899ad
Revises: 5020e5f075e6
Create Date: 2020-11-18 17:48:51.238181
"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "e166f82899ad"
down_revision = "5020e5f075e6"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("site")


def downgrade():
    op.create_table(
        "site",
        sa.Column("id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_on",
            postgresql.TIMESTAMP(),
            server_default=sa.text("timezone('utc'::text, now())"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_on",
            postgresql.TIMESTAMP(),
            server_default=sa.text("timezone('utc'::text, now())"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "data",
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("name", sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column(
            "location",
            geoalchemy2.types.Geography(
                geometry_type="POINT",
                srid=4326,
                from_text="ST_GeogFromText",
                name="geography",
            ),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("notes", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("country_id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "exposure_id", postgresql.UUID(), autoincrement=False, nullable=False
        ),
        sa.Column("project_id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "reef_type_id", postgresql.UUID(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "reef_zone_id", postgresql.UUID(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "updated_by_id", postgresql.UUID(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "predecessor_id", postgresql.UUID(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "validations",
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "created_by_id", postgresql.UUID(), autoincrement=False, nullable=False
        ),
        sa.Column("_source_id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"], ["project.id"], name="site_project_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="site_pkey"),
    )

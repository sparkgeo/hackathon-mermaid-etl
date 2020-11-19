"""empty message
# flake8: noqa
Revision ID: 5bee2a2c496d
Revises: 773a734e8e5c
Create Date: 2020-11-17 18:12:53.746663
"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5bee2a2c496d"
down_revision = "773a734e8e5c"
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.create_table(
        "project",
        sa.Column("id", postgresql.UUID(), nullable=False),
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
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("notes", sa.Text(), nullable=False),
        sa.Column("status", sa.SmallInteger(), nullable=False),
        sa.Column("updated_by_id", postgresql.UUID(), nullable=False),
        sa.Column("data_policy_beltfish", sa.SmallInteger(), nullable=False),
        sa.Column("data_policy_benthiclit", sa.SmallInteger(), nullable=False),
        sa.Column("data_policy_benthicpit", sa.SmallInteger(), nullable=False),
        sa.Column("data_policy_habitatcomplexity", sa.SmallInteger(), nullable=False),
        sa.Column("data_policy_bleachingpc", sa.SmallInteger(), nullable=False),
        sa.Column("created_by_id", postgresql.UUID(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="project_name_uniq"),
    )
    op.create_table(
        "site",
        sa.Column("id", postgresql.UUID(), nullable=False),
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
        sa.Column("predecessor_id", postgresql.UUID(), nullable=False),
        sa.Column(
            "validations", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("created_by_id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("table_01")


def downgrade():
    op.create_table(
        "table_01",
        sa.Column(
            "id",
            sa.SMALLINT(),
            server_default=sa.text("nextval('table_01_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("name", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="table_01_pkey"),
    )
    op.drop_table("site")
    op.drop_table("project")

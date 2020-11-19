"""empty message
# flake8: noqa
Revision ID: b0ecefa97eda
Revises: efe0a86d3526
Create Date: 2020-11-19 17:51:51.102740
"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from alembic_utils.pg_view import PGView


# revision identifiers, used by Alembic.
revision = "b0ecefa97eda"
down_revision = "efe0a86d3526"
branch_labels = None
depends_on = None

public_project_site = PGView(
    schema="public",
    signature="project_site",
    definition="""
SELECT p.id project_id
     , p.name project_name
     , s.name site_name
     , s.updated_on site_updated_on
     , ST_ASTEXT(s.location) site_location
  FROM project p
  JOIN site s ON s.project_id = p.id
;
        """,
)


def upgrade():
    op.replace_entity(public_project_site)


def downgrade():
    op.drop_entity(public_project_site)

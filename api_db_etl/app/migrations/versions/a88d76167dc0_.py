"""empty message
# flake8: noqa
Revision ID: a88d76167dc0
Revises: 5bee2a2c496d
Create Date: 2020-11-17 22:50:49.243475
"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from uuid import uuid4


# revision identifiers, used by Alembic.
revision = "a88d76167dc0"
down_revision = "5bee2a2c496d"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        f"""
    INSERT INTO project (id, name, notes, status, updated_by_id, data_policy_beltfish, data_policy_benthiclit, data_policy_benthicpit, data_policy_habitatcomplexity, data_policy_bleachingpc, created_by_id)
VALUES
    ('8c213ce8-7973-47a5-9359-3a0ef12ed201', 'Default Project', 'Non-nullable notes', 1, '{uuid4()}', 1, 1, 1, 1, 1, '{uuid4()}');
"""
    )


def downgrade():
    op.execute("DELETE FROM project WHERE id = '8c213ce8-7973-47a5-9359-3a0ef12ed201';")

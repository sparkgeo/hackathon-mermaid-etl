from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Table, Column, UniqueConstraint, text
from sqlalchemy.types import String, DateTime, Text, SmallInteger

from app.database import metadata


project = Table(
    "project",
    metadata,
    Column("id", UUID, primary_key=True),
    Column(
        "created_on",
        DateTime(timezone=False),
        nullable=False,
        server_default=text("(now() at time zone 'utc')"),
    ),
    Column(
        "updated_on",
        DateTime(timezone=False),
        nullable=False,
        server_default=text("(now() at time zone 'utc')"),
    ),
    Column("name", String(255), nullable=False),
    Column("notes", Text, nullable=False),
    Column("status", SmallInteger, nullable=False),
    Column("updated_by_id", UUID, nullable=False),
    Column("data_policy_beltfish", SmallInteger, nullable=False),
    Column("data_policy_benthiclit", SmallInteger, nullable=False),
    Column("data_policy_benthicpit", SmallInteger, nullable=False),
    Column("data_policy_habitatcomplexity", SmallInteger, nullable=False),
    Column("data_policy_bleachingpc", SmallInteger, nullable=False),
    Column("created_by_id", UUID),
    UniqueConstraint("name", name="project_name_uniq"),
)

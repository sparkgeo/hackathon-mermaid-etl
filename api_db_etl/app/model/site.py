from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql.json import JSONB

from sqlalchemy import Table, Column, text, ForeignKey
from sqlalchemy.types import String, DateTime, Text

from geoalchemy2 import Geography

from app.database import metadata


site = Table(
    "site",
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
    Column("data", JSONB),
    Column("name", String(255), nullable=False),
    Column("location", Geography("POINT"), nullable=False),
    Column("notes", Text, nullable=False),
    Column("country_id", UUID, nullable=False),
    Column("exposure_id", UUID, nullable=False),
    Column(
        "project_id",
        UUID,
        ForeignKey("project.id", name="site_project_id_ref_constraint"),
        nullable=False,
    ),
    Column("reef_type_id", UUID, nullable=False),
    Column("reef_zone_id", UUID, nullable=False),
    Column("updated_by_id", UUID, nullable=False),
    Column("predecessor_id", UUID),
    Column("validations", JSONB),
    Column("created_by_id", UUID, nullable=False),
)

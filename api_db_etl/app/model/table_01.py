from sqlalchemy import MetaData, Table, Column
from sqlalchemy.types import Integer, String


table_01 = Table(
    "table_01",
    MetaData(),
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
)

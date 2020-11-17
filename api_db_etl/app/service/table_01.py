from sqlalchemy import Table

from ..database import db
from ..model.table_01 import table_01


async def get_by_id(id: int):
    return await db.fetch_one(table_01.select().where(table_01.c.id == id))

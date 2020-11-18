from uuid import UUID

from ..database import db
from ..model.project import project


async def get_by_id(id: UUID):
    return await db.fetch_one(project.select().where(project.c.id == id))

from uuid import UUID

from app.database import db
from app.model.project import project


async def get_by_id(id: UUID):
    return await db.fetch_one(project.select().where(project.c.id == id))

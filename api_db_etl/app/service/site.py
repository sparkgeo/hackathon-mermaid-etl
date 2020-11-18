from uuid import UUID, uuid4
from typing import Dict

from ..database import db
from ..model.site import site


async def insert(to_insert: Dict[str, object]):
    last_record_id = await db.execute(site.insert().values(**dict({
        "id": uuid4()
    }, **to_insert)))
    return await db.fetch_one(site.select().where(site.c.id == last_record_id))

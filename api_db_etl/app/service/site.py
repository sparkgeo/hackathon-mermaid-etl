from asyncpg.exceptions import ForeignKeyViolationError
from uuid import UUID, uuid4
from typing import Dict, List

from app.ingress.constraints.db_constraint_detail import DbConstraintDetail
from app.ingress.constraints.util import get_fk_violation_detail
from app.database import db
from app.model.site import site


async def insert(to_insert: Dict[str, object]) -> DbConstraintDetail:
    try:
        last_record_id = await db.execute(site.insert().values(**dict({
            "id": uuid4()
        }, **to_insert)))
    except ForeignKeyViolationError as fke:
        return get_fk_violation_detail(site, fke, to_insert)
    # except other db problems and convert exception to DbConstraintDetail...
    await db.fetch_one(site.select().where(site.c.id == last_record_id))

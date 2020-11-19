from asyncpg.exceptions import ForeignKeyViolationError
from uuid import UUID, uuid4
from typing import Dict, List
from sqlalchemy import and_, func as sqlfunc, select
from geoalchemy2 import functions as geofunc

from app.ingress.constraints.db_constraint_detail import DbConstraintDetail
from app.ingress.constraints.util import get_fk_violation_detail
from app.ingress.validations.validation_result import ValidationResult
from app.database import db
from app.model.site import site


async def insert(to_insert: Dict[str, object]) -> DbConstraintDetail:
    try:
        last_record_id = await db.execute(site.insert().values(to_insert))
    except ForeignKeyViolationError as fke:
        return get_fk_violation_detail(site, fke, to_insert)
    # except other db problems and convert exception to DbConstraintDetail...
    await db.fetch_one(site.select().where(site.c.id == last_record_id))


async def validate(to_insert: Dict[str, object]) -> List[ValidationResult]:
    similar_sites = await db.fetch_all(
        select([
            site.c.id,
            site.c.name,
            sqlfunc.similarity(site.c.name, to_insert[site.c.name.name]).label("similarity"),
            geofunc.ST_Distance(site.c.location, to_insert[site.c.location.name])
        ]).select_from(
            site
        ).where(
            and_(
                site.c.id != to_insert[site.c.id.name],   # do not report a similarity error if it's the same record
                site.c.project_id == to_insert[site.c.project_id.name],
                sqlfunc.similarity(site.c.name, to_insert[site.c.name.name]) > 0.5,
                geofunc.ST_DWithin(site.c.location, to_insert[site.c.location.name], 100)
            )
        )
    )
    for similar_site in similar_sites:
        print(similar_site)

    return list()

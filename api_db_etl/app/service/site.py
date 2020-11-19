from asyncpg.exceptions import ForeignKeyViolationError
from typing import Dict, List
from sqlalchemy import and_, func as sqlfunc, select, inspect
from sqlalchemy.dialects.postgresql import insert
from geoalchemy2 import functions as geofunc

from app.ingress.constraints.db_constraint_detail import DbConstraintDetail
from app.ingress.constraints.util import get_fk_violation_detail
from app.ingress.validations.validation_result import ValidationResult
from app.database import db, engine
from app.model.site import site


async def upsert(to_insert: Dict[str, object]) -> DbConstraintDetail:
    try:
        upsert = (
            insert(site)
            .values(to_insert)
            .on_conflict_do_update(
                index_elements=[key.name for key in inspect(site).primary_key],
                set_=to_insert,
            )
        )
        upsert.bind = engine
        last_record_id = await db.execute(upsert)
    except ForeignKeyViolationError as fke:
        return get_fk_violation_detail(site, fke, to_insert)
    # except other db problems and convert exception to DbConstraintDetail...
    await db.fetch_one(site.select().where(site.c.id == last_record_id))


async def validate(to_insert: Dict[str, object]) -> List[ValidationResult]:
    validation_results = list()
    similar_sites = await db.fetch_all(
        select(
            [
                site.c.id,
                site.c.name,
                sqlfunc.similarity(site.c.name, to_insert[site.c.name.name]).label(
                    "similarity"
                ),
                geofunc.ST_Distance(
                    site.c.location, to_insert[site.c.location.name]
                ).label("distance"),
            ]
        )
        .select_from(site)
        .where(
            and_(
                site.c.id
                != to_insert[
                    site.c.id.name
                ],  # do not report a similarity error if it's the same record
                site.c.project_id == to_insert[site.c.project_id.name],
                sqlfunc.similarity(site.c.name, to_insert[site.c.name.name]) > 0.5,
                geofunc.ST_DWithin(
                    site.c.location, to_insert[site.c.location.name], 100
                ),  # metres
            )
        )
    )
    similar_site_report = [
        f"{site_data['name']} ({site_data['distance']}m)"
        for site_data in [dict(similar_site) for similar_site in similar_sites]
    ]
    validation_results.append(
        ValidationResult(
            column_names=[],
            description=""
            if len(similar_site_report) == 0
            else "Similar site(s) nearby: {0}".format(", ".join(similar_site_report)),
            passed=len(similar_site_report) == 0,
        )
    )

    return validation_results

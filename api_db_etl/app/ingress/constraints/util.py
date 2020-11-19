from asyncpg.exceptions import ForeignKeyViolationError
from sqlalchemy import Table
from typing import Dict

from app.ingress.constraints.db_constraint_detail import DbConstraintDetail


def get_fk_violation_detail(
    model: Table,
    exception: ForeignKeyViolationError,
    attempted_change: Dict[str, object],
) -> DbConstraintDetail:
    matching_constraints = list(
        filter(
            lambda constraint: constraint.name == exception.constraint_name,
            model.constraints,
        )
    )
    if len(matching_constraints) == 1:
        matching_constraint = matching_constraints[0]
        return DbConstraintDetail(
            column_names=matching_constraint.column_keys,
            table_name=matching_constraint.table.name,
            description="Attribute references a non-existent record",
        )
    else:
        print(
            f"unnamed constraints make it difficult to provide useful information to the caller"
        )
        return DbConstraintDetail(
            column_names=list(attempted_change.keys()),
            table_name=model.name,
            description=exception.detail,
        )

import os

from app.ingress.config_reader import load_etl_config, FieldMap
from app.ingress.conversions.geojson_to_geometry import convert as geojson_to_geometry
from app.ingress.conversions.str_to_datetime import convert as str_to_datetime
from app.ingress.exceptions.unknown_id_error import UnknownIdError
from app.ingress.import_report import ImportReport
from app.ingress.import_status import ImportStatus
from app.ingress.validations.validation_error import ValidationError
from app.ingress.validations.validation_error_type import ValidationErrorType
from app.service.couchdb import get_document_by_id, record_import_in_document
from app.service.document_management_error import DocumentManagementError
from app.service.site import upsert as upsert_site, validate as validate_site


FIELD_MAPS_BY_TABLE = load_etl_config(
    os.path.join(os.path.dirname(__file__), "config.yml")
).record_maps
FIELD_CONVERSIONS = {
    "geojson|geography": geojson_to_geometry,
    "str|datetime.datetime": str_to_datetime,
}
VALIDATIONS = {"site": validate_site}
UPSERTS = {"site": upsert_site}


async def import_document_by_id(
    target_model: str, document_id: str, ignore_optional_errors: bool
) -> ImportReport:
    try:
        record = get_document_by_id(document_id)
    except ValueError:
        raise UnknownIdError()

    import_status = ImportStatus.FAILED
    import_detail = ""
    validation_errors = list()
    to_import = dict()
    for field_name, field_value in dict(record).items():
        field_map = _get_field_map_from_source(target_model.name, field_name)
        target_value = None
        if field_map:
            if field_map.source_type and field_map.target_type:
                field_conversion_ident = (
                    f"{field_map.source_type}|{field_map.target_type}"
                )
                field_conversion = FIELD_CONVERSIONS.get(field_conversion_ident)
                if field_conversion:
                    target_value = field_conversion(field_value)
                else:
                    print(
                        f"Attempted unknown source/target conversion {field_conversion_ident}"
                    )
                    continue
            else:
                target_value = field_value
            to_import[field_map.target] = target_value

    columns_in_model = set([column.name for column in target_model.c])
    columns_in_insert = set([key for key in to_import.keys()])
    unknown_columns = columns_in_insert.difference(columns_in_model)
    if len(unknown_columns) > 0:
        raise ValueError(
            f"The following columns are mapped but unknown in the target model: {unknown_columns}"
        )

    validation_results = await VALIDATIONS[target_model.name](to_import)
    validation_failures = list(
        filter(
            lambda validation_result: not validation_result.passed, validation_results
        )
    )
    if len(validation_failures) > 0:
        for validation_failure in validation_failures:
            validation_errors.append(
                ValidationError(
                    validation_error_type=ValidationErrorType.OPTIONAL,
                    field_names=list(
                        map(
                            lambda column_name: _convert_target_field_name_to_source(
                                target_model.name, column_name
                            ),
                            validation_failure.column_names,
                        )
                    ),
                    error=validation_failure.description,
                )
            )

    if len(validation_errors) == 0 or ignore_optional_errors:
        db_constraint_detail = await UPSERTS[target_model.name](to_import)
        if db_constraint_detail:
            validation_errors.append(
                ValidationError(
                    validation_error_type=ValidationErrorType.MANDATORY,
                    field_names=list(
                        map(
                            lambda column_name: _convert_target_field_name_to_source(
                                target_model.name, column_name
                            ),
                            db_constraint_detail.column_names,
                        )
                    ),
                    error=db_constraint_detail.description,
                )
            )
        else:
            try:
                record_import_in_document(record)
                import_status = ImportStatus.COMPLETE
            except DocumentManagementError as dme:
                import_status = ImportStatus.PARTIAL
                import_detail = dme.detail

    return ImportReport(
        validation_errors=validation_errors, status=import_status, detail=import_detail,
    )


def _get_field_map_from_source(target_table: str, source_field_name: str) -> FieldMap:
    candidates = list(
        filter(
            lambda field_map: field_map.source == source_field_name,
            FIELD_MAPS_BY_TABLE[f"mermaid-{target_table}"],
        )
    )
    return candidates[0] if len(candidates) > 0 else None


def _convert_target_field_name_to_source(
    target_table: str, target_field_name: str
) -> str:
    candidates = list(
        filter(
            lambda field_map: field_map.target == target_field_name,
            FIELD_MAPS_BY_TABLE[f"mermaid-{target_table}"],
        )
    )
    if len(candidates) == 1:
        return candidates[0].source
    else:
        return target_field_name

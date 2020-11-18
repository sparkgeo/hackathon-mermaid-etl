import os

from .config_reader import load_etl_config, FieldMap
from .conversions.geojson_to_geometry import convert as geojson_to_geometry
from .conversions.str_to_datetime import convert as str_to_datetime
from ..service.couchdb import get_record_by_id
from ..service.site import insert as insert_site


FIELD_MAPS_BY_TABLE = load_etl_config(os.path.join(os.path.dirname(__file__), "config.yml")).record_maps
FIELD_CONVERSIONS = {
    "geojson|geography": geojson_to_geometry,
    "str|datetime.datetime": str_to_datetime,
}
INSERTS = {
    "site": insert_site
}

async def import_record_by_id(target_model: str, record_id: str):
    try:
        record = get_record_by_id(record_id)
    except Exception as e:
        print(f"problem retrieving record {record_id}: {e}")
        return None

    to_import = dict()
    for field_name, field_value in dict(record).items():
        field_map = _get_field_map_for_field(target_model.name, field_name)
        target_value = None
        if field_map:
            if field_map.source_type and field_map.target_type:
                field_conversion_ident = f"{field_map.source_type}|{field_map.target_type}"
                field_conversion = FIELD_CONVERSIONS.get(field_conversion_ident)
                if field_conversion:
                    target_value = field_conversion(field_value)
                else:
                    print(f"Attempted unknown source/target conversion {field_conversion_ident}")
                    continue
            else:
                target_value = field_value
            to_import[field_map.target] = target_value

    columns_in_model = set([column.name for column in target_model.c])
    columns_in_insert = set([key for key in to_import.keys()])
    unknown_columns = columns_in_insert.difference(columns_in_model)
    if len(unknown_columns) > 0:
        raise ValueError(f"The following columns are mapped but unknown in the target model: {unknown_columns}")

    await INSERTS[target_model.name](to_import)


def _get_field_map_for_field(target_table: str, field_name: str) -> FieldMap:
    candidates = list(filter(lambda field_map: field_map.source == field_name, FIELD_MAPS_BY_TABLE[f"mermaid-{target_table}"]))
    return candidates[0] if len(candidates) > 0 else None

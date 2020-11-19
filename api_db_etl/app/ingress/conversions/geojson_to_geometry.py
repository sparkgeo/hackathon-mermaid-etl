import json
from typing import Dict

from geoalchemy2.functions import ST_GeomFromGeoJSON


def convert(geojson_dict: Dict[str, object]):
    # should be converting to Geography, not Geometry, but geoalchemy does not provide ST_GeogFromGeoJSON
    # at least for point features, postgres seems happy to accept a Geometry in place of a Geography
    # if this creates problems, should parse geojson to a point object, convert point object to WKT, then call ST_GeogFromText, which is supported by geoalchemy
    return ST_GeomFromGeoJSON(json.dumps(geojson_dict))

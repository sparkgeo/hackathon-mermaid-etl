import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union

import yaml
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class FieldMap:
    source: str
    target: str
    source_type: Optional[str] = None
    target_type: Optional[str] = None


@dataclass_json
@dataclass
class ETLConfig:
    version: str
    record_maps: Dict[str, List[FieldMap]] = field(default_factory=dict)


def load_etl_config(file_path: Union[Path, str]) -> ETLConfig:
    with open(file_path) as f:
        yml_content = yaml.load(f.read(), Loader=yaml.FullLoader)
        return ETLConfig.from_dict(yml_content)


if __name__ == "__main__":
    etl_config = load_etl_config(os.path.join(os.path.dirname(__file__), "config.yml"))
    for field_map in etl_config.record_maps["mermaid-site"]:
        print(field_map.source)

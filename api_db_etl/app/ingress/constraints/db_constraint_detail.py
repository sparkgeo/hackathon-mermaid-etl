from pydantic import BaseModel
from typing import List


class DbConstraintDetail(BaseModel):
    column_names: List[str]
    table_name: str
    description: str

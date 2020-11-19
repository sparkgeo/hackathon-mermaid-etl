from pydantic import BaseModel
from typing import List


class ValidationResult(BaseModel):
    column_names: List[str]
    description: str
    passed: bool

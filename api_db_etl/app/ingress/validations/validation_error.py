from pydantic import BaseModel
from typing import List

from app.ingress.validations.validation_error_type import ValidationErrorType


class ValidationError(BaseModel):
    validation_error_type: ValidationErrorType
    field_names: List[str]
    error: str

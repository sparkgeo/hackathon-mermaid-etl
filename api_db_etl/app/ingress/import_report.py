from pydantic import BaseModel
from typing import List

from app.ingress.validations.validation_error import ValidationError


class ImportReport(BaseModel):
    validation_errors: List[ValidationError]
    success: bool

from pydantic import BaseModel
from typing import List

from app.ingress.validations.validation_error import ValidationError
from app.ingress.import_status import ImportStatus


class ImportReport(BaseModel):
    validation_errors: List[ValidationError]
    status: ImportStatus
    detail: str

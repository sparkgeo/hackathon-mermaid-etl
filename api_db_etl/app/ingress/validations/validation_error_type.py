from enum import Enum


class ValidationErrorType(Enum):
    MANDATORY = "mandatory"
    OPTIONAL = "optional"

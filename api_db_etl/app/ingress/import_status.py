from enum import Enum


class ImportStatus(Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    FAILED = "failed"

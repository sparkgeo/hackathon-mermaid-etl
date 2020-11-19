import couchdb
from datetime import datetime
from copy import deepcopy

from app.settings import COUCHDB_URL, COUCHDB_DBNAME
from app.service.document_management_error import DocumentManagementError

couchserver = couchdb.Server(COUCHDB_URL)
if COUCHDB_DBNAME in couchserver:
    db = couchserver[COUCHDB_DBNAME]
else:
    raise ValueError(f"Configured CouchDB name ({COUCHDB_DBNAME}) does not exist")


def get_document_by_id(id: str):
    if id in db:
        return db[id]
    else:
        raise ValueError(f"Expected ID is not available: {id}")


def record_import_in_document(document: object) -> None:
    try:
        document_copy = deepcopy(document)
        document_copy["imported_on"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        db.save(document_copy)
    except couchdb.ResourceConflict:
        raise DocumentManagementError(
            "The source document in couchdb changed during import. Import timestamp could not be set in document"
        )

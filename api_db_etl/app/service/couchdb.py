import couchdb

from ..settings import COUCHDB_URL, COUCHDB_DBNAME

couchserver = couchdb.Server(COUCHDB_URL)
if COUCHDB_DBNAME in couchserver:
    db = couchserver[COUCHDB_DBNAME]
else:
    raise ValueError(f"Configured CouchDB name ({COUCHDB_DBNAME}) does not exist")

def get_documents_since(since: str = "0"):
    return db.changes(since=since)


def get_record_by_id(id: str):
    if id in db:
        return db[id]
    else:
        raise ValueError(f"Expected ID is not available: {id}")
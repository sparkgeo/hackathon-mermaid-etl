import couchdb

from app.settings import COUCHDB_URL, COUCHDB_DBNAME

if __name__ == "__main__":
    try:
        couchserver = couchdb.Server(COUCHDB_URL)
        if COUCHDB_DBNAME not in couchserver:
            print(f"couchdb database {COUCHDB_DBNAME} does not yet exist")
            exit(1)
    except Exception as e:
        print(f"couchdb connection problem: {e}")
        exit(1)

    exit(0)

import couchdb

from app.settings import COUCHDB_URL

if __name__ == "__main__":
    try:
        couchserver = couchdb.Server(COUCHDB_URL)
        if not couchserver:
            print(f"couchdb server not yet available")
            exit(1)
    except Exception as e:
        print(f"couchdb connection problem: {e}")
        exit(1)

    exit(0)

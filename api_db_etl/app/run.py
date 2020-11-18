from asyncio import get_event_loop

from .ingress.import_data import import_record
from .service.couchdb import get_documents_since
from .model.site import site
from .database import db


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(db.connect())

    try:
        loop.run_until_complete(import_record(site, "bceeb72e-3ef7-4edb-b244-4ecbebfd63da"))
    except Exception as e:
        print(e)
    finally:
        loop.run_until_complete(db.disconnect())

from asyncio import get_event_loop

from .service.couchdb import get_documents_since
from .database import db


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(db.connect())

    try:
        print(f"all docs: {get_documents_since()}")
    except Exception as e:
        print(e)
    finally:
        loop.run_until_complete(db.disconnect())

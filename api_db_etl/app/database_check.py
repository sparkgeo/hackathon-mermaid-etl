import asyncio

from app.database import db

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(db.connect())
    except Exception:
        exit(1)
    loop.run_until_complete(db.disconnect())
    exit(0)

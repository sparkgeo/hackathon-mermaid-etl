from asyncio import get_event_loop

from .service.table_01 import get_by_id
from .database import db


loop = get_event_loop()
loop.run_until_complete(db.connect())
result = None #get_event_loop().run_until_complete(get_by_id(1))
if result:
    print(f"result: {dict(result)}")
else:
    print("No result")

loop.run_until_complete(db.disconnect())

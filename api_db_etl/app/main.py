import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ingress.import_data import import_record_by_id
from app.model.site import site
from app.database import db


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.post("/site/import/{record_id}")
async def import_site_record_by_id(record_id: str):
    await import_record_by_id(site, record_id)


if __name__ == "__main__":
    import sys
    import uvicorn

    port = 8888 if len(sys.argv) == 1 else int(sys.argv[1])
    print(f"Available on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

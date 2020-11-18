import logging

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from app.ingress.import_data import import_record_by_id
from app.ingress.validations.validation_error import ValidationError
from app.ingress.validations.validation_error_type import ValidationErrorType
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


@app.post("/site/import/{record_id}", response_model=List[ValidationError])
async def import_site_record_by_id(record_id: str, response: Response, force: bool = False):
    validation_errors = await import_record_by_id(site, record_id, force)
    if len(list(filter(lambda validation_error: validation_error.validation_error_type == ValidationErrorType.MANDATORY, validation_errors))) > 0:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return validation_errors


if __name__ == "__main__":
    import sys
    import uvicorn

    port = 8888 if len(sys.argv) == 1 else int(sys.argv[1])
    print(f"Available on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

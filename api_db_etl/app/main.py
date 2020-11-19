from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware

from app.ingress.import_data import import_document_by_id
from app.ingress.import_report import ImportReport
from app.ingress.import_status import ImportStatus
from app.ingress.exceptions.unknown_id_error import UnknownIdError
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

IMPORT_STATUS_MAP = {
    ImportStatus.FAILED: status.HTTP_422_UNPROCESSABLE_ENTITY,
    ImportStatus.PARTIAL: status.HTTP_207_MULTI_STATUS,
    ImportStatus.COMPLETE: status.HTTP_200_OK,
}


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.post("/site/import/{document_id}", response_model=ImportReport)
async def import_site_document_by_id(
    document_id: str, response: Response, force: bool = False
):
    try:
        import_report = await import_document_by_id(site, document_id, force)
    except UnknownIdError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document ID '{document_id}' not recognised",
        )
    response.status_code = IMPORT_STATUS_MAP[import_report.status]
    return import_report


# local debug
if __name__ == "__main__":
    import sys
    import uvicorn

    port = 8888 if len(sys.argv) == 1 else int(sys.argv[1])
    print(f"Available on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

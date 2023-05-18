import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

import logging

from src.rest.routes import router
from src.rest.model import ErrorResponse

log = logging.getLogger(__name__)

app = FastAPI(
    title="ValueSets API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/docs/openapi.json",
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=origins,
)
app.include_router(router)


@app.exception_handler(500)
async def error_500(_: Request, error: HTTPException):
    log.error(
        "500 - Internal Server Error",
        exc_info=(type(error), error, error.__traceback__),
    )

    return ErrorResponse(
        status_code=500,
        message="Internal Server Error",
    )


def start():
    uvicorn.run("src.rest.server:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start()

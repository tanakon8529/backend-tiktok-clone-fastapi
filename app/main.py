from fastapi import FastAPI
from datetime import datetime
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app.settings.configs import API_VERSION, API_PATH, API_DOC
from app.endpoint import api_router

from app.middleware import DBSessionMiddleware
from app.utilities.database_util import url_database

stamp_today = datetime.now()
today = stamp_today.strftime("%Y%m%d")
path_log = "./app/log/{}.log".format(today)
logger.add(path_log, encoding='utf-8', enqueue=True, diagnose=True)
logger.debug(path_log)

app = FastAPI(
    title="Client Gateway API",
    description="Client Gateway API",
    version=API_VERSION,
    docs_url=API_DOC,
    redoc_url=None,
    openapi_url=f"{API_DOC}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(DBSessionMiddleware, db_url=url_database())
app.include_router(api_router, prefix=API_PATH)
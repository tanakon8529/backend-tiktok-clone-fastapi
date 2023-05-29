from __future__ import annotations

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Any
from loguru import logger
from datetime import datetime

from app.apis.feed.submod import get_init_feed_by_payload

def get_init_feed(payload: dict, db_session: Session):

    try:
        result = get_init_feed_by_payload(payload, db_session)
        if result == None:
            raise HTTPException(status_code=404, detail='Not Found')
        if "error_code" in result:
            raise HTTPException(status_code=400, detail='{}'.format(result["msg"]))
        if "error_server" in result:
            raise HTTPException(status_code=500, detail='{}'.format(result["msg"]))

        return result
    except Exception as e:
        logger.error(f"{e}")
        if isinstance(e, HTTPException):
            raise
        else:
            raise HTTPException(status_code=500, detail='internal server error: {0}'.format(e))
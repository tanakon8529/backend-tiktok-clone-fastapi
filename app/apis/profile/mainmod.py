from __future__ import annotations

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Any
from loguru import logger
from datetime import datetime

from app.apis.profile.submod import get_login_profile_by_mail, get_login_profile_by_mobile, \
                        get_login_profile_by_key


def get_login_profile_mail(db_session: Session, payload: Any):

    try:
        result = None
        if payload.email:
            result = get_login_profile_by_mail(db_session, payload)
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


def get_login_profile_mobile(db_session: Session, payload: Any):

    try:
        result = None
        if payload.mobile_phone_number:
            result = get_login_profile_by_mobile(db_session, payload)
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
        

def get_login_profile_key(db_session: Session, payload: Any):

    try:
        result = None
        if payload.cookie_cache_key:
            result = get_login_profile_by_key(db_session, payload)
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
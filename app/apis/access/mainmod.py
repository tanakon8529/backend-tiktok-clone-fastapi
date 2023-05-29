from __future__ import annotations

from fastapi import HTTPException
from loguru import logger

from app.core.auth import authenticate_user, store_access_token

def get_token(client_id, client_secret):

    try:
        access_token = authenticate_user(client_id, client_secret)
        if not access_token:
            raise HTTPException(status_code=401, detail='Access Denied')
        
        result = store_access_token(access_token)
        if isinstance(result, Exception):
            raise HTTPException(status_code=500, detail='{}'.format(result["msg"]))

        return result
    except Exception as e:
        logger.error(f"{e}")
        if isinstance(e, HTTPException):
            raise
        else:
            raise HTTPException(status_code=500, detail='internal server error: {0}'.format(e))
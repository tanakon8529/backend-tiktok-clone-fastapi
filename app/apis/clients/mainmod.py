from __future__ import annotations

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Any
from loguru import logger

from app.apis.clients.submod import sending_smtp_mail_otp_by_email, verify_smtp_mail_otp_by_email, \
                                sending_mobile_sms_otp_by_mobile_phone_number, verify_mobile_sms_otp_by_mobile_phone_number

def sending_smtp_mail_otp(payload: Any):

    try:
        result = None
        if payload.email:
            result = sending_smtp_mail_otp_by_email(payload.email)
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
        
def verify_smtp_mail_otp(db_session: Session, payload: Any):

    try:
        result = None
        if payload.email:
            result = verify_smtp_mail_otp_by_email(db_session, payload)
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

def sending_mobile_sms_otp(payload: Any):

    try:
        result = None
        if payload.mobile_phone_number:
            result = sending_mobile_sms_otp_by_mobile_phone_number(payload.mobile_phone_number)
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
        
def verify_mobile_sms_otp(db_session: Session, payload: Any):

    try:
        result = None
        if payload.mobile_phone_number:
            result = verify_mobile_sms_otp_by_mobile_phone_number(db_session, payload)
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
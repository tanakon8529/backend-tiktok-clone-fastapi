from __future__ import annotations

from fastapi import APIRouter, Depends

from app.middleware import db
from app.core.auth import valid_access_token
from app.apis.clients.mainmod import sending_smtp_mail_otp, verify_smtp_mail_otp, sending_mobile_sms_otp, verify_mobile_sms_otp
from app.apis.clients.model import verify_mail_otp_model, verify_sms_otp_model

router = APIRouter()

@router.post("/v1/mail/send")
async def sending_mail_otp(
    payload: verify_mail_otp_model,
    token: str = Depends(valid_access_token)
):  
    return sending_smtp_mail_otp(payload)

@router.post("/v1/mail/verify")
async def verify_mail_otp(
    payload: verify_mail_otp_model,
    token: str = Depends(valid_access_token)
):  
    db_session = db.session
    return verify_smtp_mail_otp(db_session, payload)

@router.post("/v1/sms/send")
async def sending_sms_otp(
    payload: verify_sms_otp_model,
    token: str = Depends(valid_access_token)
):  
    return sending_mobile_sms_otp(payload)

@router.post("/v1/sms/verify")
async def verify_sms_otp(
    payload: verify_sms_otp_model,
    token: str = Depends(valid_access_token)
):  
    db_session = db.session
    return verify_mobile_sms_otp(db_session, payload)

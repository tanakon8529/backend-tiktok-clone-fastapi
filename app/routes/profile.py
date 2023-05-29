from __future__ import annotations

from fastapi import APIRouter, Depends, Header

from app.middleware import db
from app.core.auth import valid_access_token
from app.apis.profile.mainmod import get_login_profile_mail, get_login_profile_mobile, \
                        get_login_profile_key

from app.apis.profile.model import login_mail_model, login_mobile_model, cookie_cache_key_model

router = APIRouter()

@router.post("/v1/login/mail")
async def login_profile_mail(
    payload: login_mail_model,
    token: str = Depends(valid_access_token)
):  
    db_session = db.session
    return get_login_profile_mail(db_session, payload)

@router.post("/v1/login/mobile")
async def login_profile_mobile(
    payload: login_mobile_model,
    token: str = Depends(valid_access_token)
):  
    db_session = db.session
    return get_login_profile_mobile(db_session, payload)

@router.post("/v1/login/key")
async def login_profile_key(
    payload: cookie_cache_key_model,
    token: str = Depends(valid_access_token)
):  
    db_session = db.session
    return get_login_profile_key(db_session, payload)

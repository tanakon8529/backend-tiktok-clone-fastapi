from __future__ import annotations

from fastapi import APIRouter, Depends, Header

from app.middleware import db
from app.core.auth import valid_access_token
from app.apis.inbox.mainmod import get_all_inbox_by_profile_uuid, get_all_user_history_by_message_uuid, get_all_group_history_by_group_uuid

router = APIRouter()

@router.get("/v1")
async def get_inbox_by_profile_uuid(
    profile_name_uuid: str,
    token: str = Depends(valid_access_token)
):  
    db_session = db.session
    return get_all_inbox_by_profile_uuid(db_session, profile_name_uuid)

@router.get("/v1/user")
async def get_user_history_by_message_uuid(
    message_uuid: str,
    token: str = Depends(valid_access_token)
):  
    db_session = db.session
    return get_all_user_history_by_message_uuid(db_session, message_uuid)

@router.get("/v1/group")
async def get_group_history_by_group_uuid(
    group_informaion_uuid: str,
    token: str = Depends(valid_access_token)
):  
    db_session = db.session
    return get_all_group_history_by_group_uuid(db_session, group_informaion_uuid)

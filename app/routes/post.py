from __future__ import annotations

from fastapi import APIRouter, Depends, Header

from app.middleware import db
from app.core.auth import valid_access_token
from app.apis.post.mainmod import get_all_post

router = APIRouter()

@router.get("/v1/post")
async def get_post(
    token: str = Depends(valid_access_token)
):  
    db_session = db.session
    return get_all_post(db_session)

from __future__ import annotations

from fastapi import APIRouter, Depends, Header

from app.middleware import db
from app.core.auth import valid_access_token
from app.apis.feed.mainmod import get_init_feed

router = APIRouter()

@router.post("/v1")
async def get_feed(
    payload: dict = {},
    token: str = Depends(valid_access_token)
):  
    db_session = db.session
    return get_init_feed(payload, db_session)

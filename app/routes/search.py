from __future__ import annotations

from fastapi import APIRouter, Depends, Header


from app.middleware import db
from app.core.auth import valid_access_token
from app.apis.search.mainmod import get_all_search

router = APIRouter()

@router.get("/v1")
async def get_search(
    type_search: str,
    text_seatch: str,
    token: str = Depends(valid_access_token),
):  
    db_session = db.session
    return get_all_search(db_session, type_search, text_seatch)

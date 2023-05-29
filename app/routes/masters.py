from __future__ import annotations

from fastapi import APIRouter, Depends, Header

from app.middleware import db
from app.core.auth import valid_access_token
from app.apis.masters.mainmod import get_all_countries

router = APIRouter()

@router.get("/v1/countries")
async def get_countries(
    token: str = Depends(valid_access_token)
):  
    db_session = db.session
    return get_all_countries(db_session)

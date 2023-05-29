from __future__ import annotations

from fastapi import APIRouter, Depends, Header

router = APIRouter()

@router.get("")
async def hello(
):
    return "Hello World!"

from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from typing import List

from app.middleware import db
from app.core.auth import valid_access_token

from app.apis.attachment.mainmod import upload_attachment_profile_s3, upload_attachment_group_s3, \
                            delete_attachment_s3
from app.apis.attachment.submod import get_session_aws
from app.apis.attachment.model import UploadFileBase, Delete_Pack_Model

router = APIRouter()

@router.post("/v1/profile")
async def upload_attachment_profile(
    payload: UploadFileBase,
    files: List[UploadFile] = File(...),
    token: str = Depends(valid_access_token),
    aws_session: Session = Depends(get_session_aws)
):
    db_session = db.session
    return upload_attachment_profile_s3(payload, files, aws_session, db_session)

@router.post("/v1/group")
async def upload_attachment_group(
    payload: UploadFileBase,
    files: List[UploadFile] = File(...),
    token: str = Depends(valid_access_token),
    aws_session: Session = Depends(get_session_aws)
):
    db_session = db.session
    return upload_attachment_group_s3(payload, files, aws_session, db_session)

@router.delete("/v1")
async def delete_attachment(
    payload: Delete_Pack_Model,
    token: str = Depends(valid_access_token),
    aws_session: Session = Depends(get_session_aws)
):
    db_session = db.session
    return delete_attachment_s3(payload, aws_session, db_session)

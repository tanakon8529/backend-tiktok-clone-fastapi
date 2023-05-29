from __future__ import annotations

from sqlalchemy.orm import Session
from fastapi import HTTPException
from loguru import logger
from datetime import datetime

from app.apis.attachment.submod import upload_attachment_profile_to_s3, upload_attachment_group_to_s3, delete_file_attachments

def upload_attachment_profile_s3(payload, files, aws_session: Session, db_session: Session):

    try:
        today = datetime.now()
        result = None
        if payload:
            result = upload_attachment_profile_to_s3(today, payload, files, aws_session, db_session)
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

def upload_attachment_group_s3(payload, files, aws_session: Session, db_session: Session):

    try:
        today = datetime.now()
        result = None
        if payload:
            result = upload_attachment_group_to_s3(today, payload, files, aws_session, db_session)
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

def delete_attachment_s3(payload, aws_session: Session, db_session: Session):

    try:
        result = None
        if payload:
            result = delete_file_attachments(payload, aws_session, db_session)
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
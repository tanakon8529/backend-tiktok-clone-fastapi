from sqlalchemy import func, or_, and_
from loguru import logger

from app.core.db_model import ClipsProfile
from app.apis.clients.model import clips_profile_base_model

import random

def get_clips_profile_random(db_session):
    session_clips_profile = db_session.query(ClipsProfile).order_by(func.random()).limit(10)
    result_clips_profile = []
    for i in session_clips_profile:
        x = clips_profile_base_model(**i.__dict__)
        result_clips_profile.append(x)
        
    return session_clips_profile, result_clips_profile

def get_clips_profile_by_clips_profile_uuid(clips_profile_uuid, db_session):
    session_clips_profile = db_session.query(ClipsProfile).filter(ClipsProfile.clips_profile_uuid==clips_profile_uuid)
    result_clips_profile = []
    for i in session_clips_profile:
        x = clips_profile_base_model(**i.__dict__)
        result_clips_profile.append(x)
        
    if result_clips_profile:
        result_clips_profile = result_clips_profile[0]
    return session_clips_profile, result_clips_profile

def get_clips_profile_by_profile_name_uuid(profile_name_uuid, db_session):
    session_clips_profile = db_session.query(ClipsProfile).filter(ClipsProfile.profile_name_uuid==profile_name_uuid).order_by(ClipsProfile.create_date.desc()).all()
    result_clips_profile = []
    for i in session_clips_profile:
        x = clips_profile_base_model(**i.__dict__)
        result_clips_profile.append(x)

    return session_clips_profile, result_clips_profile

def fill_create_clips_profile(today, payload):
    
    item_clips_profile = ClipsProfile(
        clips_profile_uuid = payload["clips_profile_uuid"],
        create_date = today,
        modified_date = today,
        profile_name_uuid = payload["profile_name_uuid"],
        file_name = payload["file_name"],
        file_type = payload["file_type"],
        file_size_kb = payload["file_size_kb"],
        file_key_s3 = payload["file_key_s3"],
        file_url_s3 = payload["file_url_s3"],
        file_url_expire_date_s3 = payload["file_url_expire_date_s3"]
    )

    return item_clips_profile

def edit_clips_profile(today, clips_profile, payload, db_session):
    data_updates = {
        "modified_date": today,
        "profile_name_uuid": payload["profile_name_uuid"],
        "file_name": payload["file_name"],
        "file_type": payload["file_type"],
        "file_size_kb": payload["file_size_kb"],
        "file_key_s3": payload["file_key_s3"],
        "file_url_s3": payload["file_url_s3"],
        "file_url_expire_date_s3": payload["file_url_expire_date_s3"]
    }

    clips_profile.update(data_updates)
    db_session.flush()
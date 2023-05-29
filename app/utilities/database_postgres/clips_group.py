from sqlalchemy import or_, and_
from loguru import logger

from app.core.db_model import ClipsGroup
from app.apis.clients.model import clips_group_base_model

def get_clips_group_by_clips_group_uuid(clips_group_uuid, db_session):
    session_clips_group = db_session.query(ClipsGroup).filter(ClipsGroup.clips_group_uuid==clips_group_uuid)
    result_clips_group = []
    for i in session_clips_group:
        x = clips_group_base_model(**i.__dict__)
        result_clips_group.append(x)

    if result_clips_group:
        result_clips_group = result_clips_group[0]
    return session_clips_group, result_clips_group

def get_clips_group_by_group_name_uuid(group_name_uuid, db_session):
    session_clips_group = db_session.query(ClipsGroup).filter(ClipsGroup.group_name_uuid==group_name_uuid)
    result_clips_group = []
    for i in session_clips_group:
        x = clips_group_base_model(**i.__dict__)
        result_clips_group.append(x)

    if result_clips_group:
        result_clips_group = result_clips_group[0]
    return session_clips_group, result_clips_group

def fill_create_clips_group(today, payload):
    
    item_clips_group = ClipsGroup(
        clips_group_uuid = payload["clips_group_uuid"],
        create_date = today,
        modified_date = today,
        group_name_uuid = payload["group_name_uuid"],
        file_name = payload["file_name"],
        file_type = payload["file_type"],
        file_size_kb = payload["file_size_kb"],
        file_key_s3 = payload["file_key_s3"],
        file_url_s3 = payload["file_url_s3"],
        file_url_expire_date_s3 = payload["file_url_expire_date_s3"]
    )

    return item_clips_group

def edit_clips_group(today, clips_group, payload, db_session):
    data_updates = {
        "modified_date": today,
        "group_name_uuid": payload["group_name_uuid"],
        "file_name": payload["file_name"],
        "file_type": payload["file_type"],
        "file_size_kb": payload["file_size_kb"],
        "file_key_s3": payload["file_key_s3"],
        "file_url_s3": payload["file_url_s3"],
        "file_url_expire_date_s3": payload["file_url_expire_date_s3"]
    }

    clips_group.update(data_updates)
    db_session.flush()
from sqlalchemy import func, or_, and_
from loguru import logger

from app.core.db_model import UserActivity
from app.apis.clients.model import user_activity_base_model

def get_user_activity_by_clips_group_uuid(clips_group_uuid, db_session):
    session_user_activity = db_session.query(UserActivity).filter(UserActivity.clips_group_uuid==clips_group_uuid)
    result_user_activity = []
    for i in session_user_activity:
        x = user_activity_base_model(**i.__dict__)
        result_user_activity.append(x)
        
    if result_user_activity:
        result_user_activity = result_user_activity[0]
    return session_user_activity, result_user_activity

def fill_create_user_activity(today, payload):
    
    item_user_activity = UserActivity(
        user_activity_uuid = payload["user_activity_uuid"],
        profile_name_uuid = payload["profile_name_uuid"],
        create_date = today,
        modified_date = today,
        content = payload["content"],
        likes = payload["likes"],
        clips_group_uuid = payload["clips_group_uuid"],
        images_group_uuid = payload["images_group_uuid"],
    )

    return item_user_activity

def edit_user_activity(today, user_activity, payload, db_session):
    data_updates = {
        "user_activity_uuid" : payload["user_activity_uuid"],
        "profile_name_uuid" : payload["profile_name_uuid"],
        "modified_date" : today,
        "content" : payload["content"],
        "likes" : payload["likes"],
        "clips_group_uuid" : payload["clips_group_uuid"],
        "images_group_uuid" : payload["images_group_uuid"],
    }

    user_activity.update(data_updates)
    db_session.flush()
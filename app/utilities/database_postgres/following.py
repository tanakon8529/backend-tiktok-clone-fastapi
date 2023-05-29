from sqlalchemy import or_, and_
from loguru import logger

from app.core.db_model import Following
from app.apis.clients.model import following_base_model

def get_following_total(profile_name_uuid, db_session):
    session_following = db_session.query(Following).filter(Following.profile_name_uuid==profile_name_uuid).order_by(Following.create_date.desc()).all()
    result_following = []
    for i in session_following:
        x = following_base_model(**i.__dict__)
        result_following.append(x)

    return session_following, result_following

def get_following_by_profile_name_uuid(profile_name_uuid, db_session):
    session_following = db_session.query(Following).filter(Following.profile_name_uuid==profile_name_uuid)
    result_following = []
    for i in session_following:
        x = following_base_model(**i.__dict__)
        result_following.append(x)

    return session_following, result_following

def fill_create_following(today, payload):
    
    item_following = Following(
        profile_name_uuid = payload["profile_name_uuid"],
        following_profile_uuid = payload["following_profile_uuid"],
        create_date = today
    )

    return item_following
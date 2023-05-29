from sqlalchemy import or_, and_
from loguru import logger

from app.core.db_model import UserProfile
from app.apis.clients.model import user_profile_base_model

def login_user_profile_by_cookie_cache_key(cookie_cache_key, db_session):
    session_user_profile = db_session.query(UserProfile).filter(UserProfile.cookie_cache_key==cookie_cache_key)
    result_user_profile = []
    for i in session_user_profile:
        x = user_profile_base_model(**i.__dict__)
        result_user_profile.append(x)

    if result_user_profile:
        result_user_profile = result_user_profile[0]
    return session_user_profile, result_user_profile

def get_user_profile_by_profile_name_uuid(profile_name_uuid, db_session):
    session_user_profile = db_session.query(UserProfile).filter(UserProfile.profile_name_uuid==profile_name_uuid)
    result_user_profile = []
    for i in session_user_profile:
        x = user_profile_base_model(**i.__dict__)
        result_user_profile.append(x)

    if result_user_profile:
        result_user_profile = result_user_profile[0]
    return session_user_profile, result_user_profile

def fill_create_user_profile(today, payload):

    item_user_profile = UserProfile(
        profile_name_uuid = payload["profile_name_uuid"],
        profile_name = payload["profile_name"],
        images_profile_uuid = payload["images_profile_uuid"],
        create_date = today,
        modified_date = today,
        username = payload["username"],
        bio = payload["bio"],
        latitude = payload["latitude"],
        longitude = payload["longitude"],
        interests = payload["interests"]
    )

    return item_user_profile

def edit_user_profile(today, user_profile, payload, db_session):
    data_updates = {
        "profile_name_uuid": payload["profile_name_uuid"],
        "profile_name": payload["profile_name"],
        "images_profile_uuid": payload["images_profile_uuid"],
        "username": payload["username"],
        "bio": payload["bio"],
        "latitude": payload["latitude"],
        "longitude": payload["longitude"],
        "interests": payload["interests"],
        "modified_date": today
    }

    user_profile.update(data_updates)
    db_session.flush()

def stamp_cookie_cache_key(today, user_profile, cookie_cache_key, db_session):
    data_updates = {
        "cookie_cache_key": cookie_cache_key,
        "modified_date": today
    }

    user_profile.update(data_updates)
    db_session.flush()
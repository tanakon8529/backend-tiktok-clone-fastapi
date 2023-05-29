from sqlalchemy import or_, and_
from loguru import logger

from app.core.db_model import ImagesProfile
from app.apis.clients.model import images_profile_base_model

def get_images_profile_by_images_profile_uuid(images_profile_uuid, db_session):
    session_images_profile = db_session.query(ImagesProfile).filter(ImagesProfile.images_profile_uuid==images_profile_uuid)
    result_images_profile = []
    for i in session_images_profile:
        x = images_profile_base_model(**i.__dict__)
        result_images_profile.append(x)

    if result_images_profile:
        result_images_profile = result_images_profile[0]
    return session_images_profile, result_images_profile

def get_images_profile_by_profile_name_uuid(profile_name_uuid, db_session):
    session_images_profile = db_session.query(ImagesProfile).filter(ImagesProfile.profile_name_uuid==profile_name_uuid)
    result_images_profile = []
    for i in session_images_profile:
        x = images_profile_base_model(**i.__dict__)
        result_images_profile.append(x)

    if result_images_profile:
        result_images_profile = result_images_profile[0]
    return session_images_profile, result_images_profile

def fill_create_images_profile(today, payload):
    
    item_images_profile = ImagesProfile(
        images_profile_uuid = payload["images_profile_uuid"],
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

    return item_images_profile

def edit_images_profile(today, images_profile, payload, db_session):
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

    images_profile.update(data_updates)
    db_session.flush()
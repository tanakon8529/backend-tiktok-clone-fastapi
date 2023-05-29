from sqlalchemy import or_, and_
from loguru import logger

from app.core.db_model import ImagesGroup
from app.apis.clients.model import images_group_base_model

def get_images_group_by_images_group_uuid(images_group_uuid, db_session):
    session_images_group = db_session.query(ImagesGroup).filter(ImagesGroup.images_group_uuid==images_group_uuid)
    result_images_group = []
    for i in session_images_group:
        x = images_group_base_model(**i.__dict__)
        result_images_group.append(x)

    if result_images_group:
        result_images_group = result_images_group[0]
    return session_images_group, result_images_group

def get_images_group_by_group_name_uuid(group_name_uuid, db_session):
    session_images_group = db_session.query(ImagesGroup).filter(ImagesGroup.group_name_uuid==group_name_uuid)
    result_images_group = []
    for i in session_images_group:
        x = images_group_base_model(**i.__dict__)
        result_images_group.append(x)

    if result_images_group:
        result_images_group = result_images_group[0]
    return session_images_group, result_images_group

def fill_create_images_group(today, payload):
    
    item_images_group = ImagesGroup(
        images_group_uuid = payload["images_group_uuid"],
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

    return item_images_group

def edit_images_group(today, images_group, payload, db_session):
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

    images_group.update(data_updates)
    db_session.flush()
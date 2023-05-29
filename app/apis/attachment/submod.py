from __future__ import annotations

import time

from loguru import logger

from app.core.db_model import ImagesProfile, ImagesGroup, ClipsGroup, ClipsProfile

from app.utilities.database_postgres.images_profile import  get_images_profile_by_images_profile_uuid, fill_create_images_profile
from app.utilities.database_postgres.clips_profile import  get_clips_profile_by_clips_profile_uuid, fill_create_clips_profile
from app.utilities.database_postgres.images_group import  get_images_group_by_images_group_uuid, fill_create_images_group
from app.utilities.database_postgres.clips_group import  get_clips_group_by_clips_group_uuid, fill_create_clips_group
from app.utilities.uuid_util import generator_uuid4
from app.utilities.amazon.s3_util import s3_control
aws = s3_control()

def get_session_aws():
    aws_session = aws.aws_s3_connect()
    return aws_session

def upload_attachment_profile_to_s3(today, payload, files, aws_session, db_session):
    logger.debug(payload)
    # Start the timer
    start_time = time.time()

    try:
        if payload.uploadtype == "images":
            result_upload_aws_s3_pack = aws.upload_images_profile_attachment(today, payload, files, aws_session)
        elif payload.uploadtype == "clips":
            result_upload_aws_s3_pack = aws.upload_clips_profile_attachment(today, payload, files, aws_session)
        else:
            return {"error_server": "01","msg": "Server is not ready, please try again."}
        
        if "error_server" in result_upload_aws_s3_pack:
            return result_upload_aws_s3_pack

        result_attachment = []
        for result_upload_s3 in result_upload_aws_s3_pack:
            
            if payload.uploadtype == "images" and result_upload_s3["status_upload"] == True:
                timeout = time.time() + 4  # set timeout to 4 seconds
                while time.time() < timeout:
                    images_profile_uuid = generator_uuid4()
                    _, result_user_profile = get_images_profile_by_images_profile_uuid(images_profile_uuid, db_session)

                    if result_user_profile == []:
                        break

                    if time.time() > 2:
                        result = {"error_server": "01","msg": "Server is not ready, please try again."}
                        return result
                    
                payload_images_profile = {
                    "images_profile_uuid" : images_profile_uuid,
                    "profile_name_uuid" : result_upload_s3["profile_name_uuid"],
                    "file_name" : result_upload_s3["file_name"],
                    "file_type" : result_upload_s3["file_type"],
                    "file_size_kb" : result_upload_s3["file_size_kb"],
                    "file_key_s3" : result_upload_s3["file_key_s3"],
                    "file_url_s3" : result_upload_s3["file_url_s3"],
                    "file_url_expire_date_s3" : result_upload_s3["file_url_expire_date_s3"],
                    "status_upload": result_upload_s3["status_upload"]
                }

                item_images_profile = fill_create_images_profile(today, payload_images_profile)
                db_session.add(item_images_profile)
                db_session.flush()

                result_attachment.append(payload_images_profile)
                
            elif payload.uploadtype == "clips" and result_upload_s3["status_upload"] == True:
                timeout = time.time() + 4  # set timeout to 4 seconds
                while time.time() < timeout:
                    clips_profile_uuid = generator_uuid4()
                    _, result_user_profile = get_clips_profile_by_clips_profile_uuid(clips_profile_uuid, db_session)

                    if result_user_profile == []:
                        break

                    if time.time() > 2:
                        result = {"error_server": "01","msg": "Server is not ready, please try again."}
                        return result
                
                payload_clips_profile = {
                    "clips_profile_uuid" : clips_profile_uuid,
                    "profile_name_uuid" : result_upload_s3["profile_name_uuid"],
                    "file_name" : result_upload_s3["file_name"],
                    "file_type" : result_upload_s3["file_type"],
                    "file_size_kb" : result_upload_s3["file_size_kb"],
                    "file_key_s3" : result_upload_s3["file_key_s3"],
                    "file_url_s3" : result_upload_s3["file_url_s3"],
                    "file_url_expire_date_s3" : result_upload_s3["file_url_expire_date_s3"],
                    "status_upload": result_upload_s3["status_upload"]
                }

                item_clips_profile = fill_create_clips_profile(today, payload_clips_profile)
                db_session.add(item_clips_profile)
                db_session.flush()

                result_attachment.append(payload_clips_profile)

        # Calculate the elapsed time
        elapsed_time = time.time() - start_time
        logger.debug(f"elapsed_time : {elapsed_time}")
        db_session.commit()
    except Exception as e:
        logger.error(e)
        result_attachment = {"error_code": "01","msg": e}
    
    return result_attachment

def upload_attachment_group_to_s3(today, payload, files, aws_session, db_session):
    logger.debug(payload)
    try:
        if payload.uploadtype == "images":
            result_upload_aws_s3_pack = aws.upload_images_group_attachment(today, payload, files, aws_session)
        elif payload.uploadtype == "clips":
            result_upload_aws_s3_pack = aws.upload_clips_group_attachment(today, payload, files, aws_session)
        else:
            return {"error_server": "01","msg": "Server is not ready, please try again."}

        if "error_server" in result_upload_aws_s3_pack:
            return result_upload_aws_s3_pack

        result_attachment = []
        for result_upload_s3 in result_upload_aws_s3_pack:
            
            if payload.uploadtype == "images" and result_upload_s3["status_upload"] == True:
                timeout = time.time() + 4  # set timeout to 4 seconds
                while time.time() < timeout:
                    images_group_uuid = generator_uuid4()
                    _, result_user_group = get_images_group_by_images_group_uuid(images_group_uuid, db_session)

                    if result_user_group == []:
                        break

                    if time.time() > 2:
                        result = {"error_server": "01","msg": "Server is not ready, please try again."}
                        return result
                    
                payload_images_group = {
                    "images_group_uuid" : images_group_uuid,
                    "group_name_uuid" : result_upload_s3["group_name_uuid"],
                    "file_name" : result_upload_s3["file_name"],
                    "file_type" : result_upload_s3["file_type"],
                    "file_size_kb" : result_upload_s3["file_size_kb"],
                    "file_key_s3" : result_upload_s3["file_key_s3"],
                    "file_url_s3" : result_upload_s3["file_url_s3"],
                    "file_url_expire_date_s3" : result_upload_s3["file_url_expire_date_s3"],
                    "status_upload": result_upload_s3["status_upload"]
                }

                item_images_group = fill_create_images_group(today, payload_images_group)
                db_session.add(item_images_group)
                db_session.flush()

                result_attachment.append(payload_images_group)
                
            elif payload.uploadtype == "clips" and result_upload_s3["status_upload"] == True:
                timeout = time.time() + 4  # set timeout to 4 seconds
                while time.time() < timeout:
                    clips_group_uuid = generator_uuid4()
                    _, result_user_group = get_clips_group_by_clips_group_uuid(clips_group_uuid, db_session)

                    if result_user_group == []:
                        break

                    if time.time() > 2:
                        result = {"error_server": "01","msg": "Server is not ready, please try again."}
                        return result
                
                payload_clips_group = {
                    "clips_group_uuid" : clips_group_uuid,
                    "group_name_uuid" : result_upload_s3["group_name_uuid"],
                    "file_name" : result_upload_s3["file_name"],
                    "file_type" : result_upload_s3["file_type"],
                    "file_size_kb" : result_upload_s3["file_size_kb"],
                    "file_key_s3" : result_upload_s3["file_key_s3"],
                    "file_url_s3" : result_upload_s3["file_url_s3"],
                    "file_url_expire_date_s3" : result_upload_s3["file_url_expire_date_s3"],
                    "status_upload": result_upload_s3["status_upload"]
                }

                item_clips_group = fill_create_clips_group(today, payload_clips_group)
                db_session.add(item_clips_group)
                db_session.flush()

                result_attachment.append(payload_clips_group)

        db_session.commit()
    except Exception as e:
        logger.error(e)
        result_attachment = {"error_code": "01","msg": e}
    
    return result_attachment

def delete_file_attachments(payload_pack, aws_session, db_session):
    logger.debug(payload_pack)
    payload = payload_pack.details_delete
    result_delete_pack = []
    result_delete = {}
    status_delete_db = False

    type_table = payload_pack.uploadtype
    if "images" in type_table:
        file_type = True
    elif "clips" in type_table:
        file_type = False

    for file_detail in payload:
        try:
            result_delete = {
                "file_name" : file_detail.file_name,
                "status_delete" : False
            }

            if type_table == "images_profile" and file_detail.images_profile_uuid:
                db_session.query(ImagesProfile).filter(ImagesProfile.images_profile_uuid==file_detail.images_profile_uuid).delete()
                status_delete_db = True
            elif type_table == "images_group" and file_detail.images_group_uuid:
                db_session.query(ImagesGroup).filter(ImagesGroup.images_group_uuid==file_detail.images_group_uuid).delete()
                status_delete_db = True
            elif type_table == "clips_group" and file_detail.clips_group_uuid:
                db_session.query(ClipsGroup).filter(ClipsGroup.clips_group_uuid==file_detail.clips_group_uuid).delete()
                status_delete_db = True
            elif type_table == "clips_profile" and file_detail.clips_profile_uuid:
                db_session.query(ClipsProfile).filter(ClipsProfile.clips_profile_uuid==file_detail.clips_profile_uuid).delete()
                status_delete_db = True

            # Delete the object from AWS S3
            if status_delete_db:
                result_delete = aws.delete_object_s3_by_key(file_detail, file_type, aws_session)
                db_session.commit()

            result_delete_pack.append(result_delete)

        except Exception as e:
            logger.error(e)
            result_delete["error_code"] = "01"
            result_delete["detail"] = e
            result_delete_pack.append(result_delete)

    return result_delete_pack
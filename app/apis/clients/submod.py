from __future__ import annotations

import time

from loguru import logger
from datetime import datetime

from app.utilities.database_postgres.personal_information import fill_create_personal_information, get_personal_information_by_email, \
                                        get_personal_information_by_mobile_phone_number

from app.utilities.database_postgres.user_profile import fill_create_user_profile, get_user_profile_by_profile_name_uuid

from app.utilities.uuid_util import generator_uuid4

from app.utilities.amazon.ses_util import ses_control
ses = ses_control()

from app.utilities.amazon.sns_util import sns_control
sns = sns_control()

def sending_smtp_mail_otp_by_email(email):
    result = None
    try:
        logger.debug(email)
        result = ses.send_email(email)
        if "error_code" in result:
            return result
        elif "success_code" in result:
            result = {"detail" : result["msg"]}

    except Exception as e:
        logger.error(e)
        result = {"error_code": "02","msg": e}

    logger.debug(result)
    return result

def verify_smtp_mail_otp_by_email(db_session, payload):
    result = None
    today = datetime.now()
    try:
        email = payload.email
        logger.debug(email)
        redis_client, result = ses.check_otp(email, payload.otp_key)
        if "error_code" in result:
            return result
        elif "success_code" in result:
            payload = {
                # user_profile
                "profile_name_uuid": None,
                "profile_name": None,
                "images_profile_uuid": None,
                "username": None,
                "bio": None,
                "latitude": None,
                "longitude": None,
                "interests": None,
                "personal_information": None,
                "transaction_history": None,
                "social_graph": None,
                "clips_and_images": None,
                "message_chat": None,

                # personal_information
                "gender": None,
                "email": email,
                "mobile_phone_number": None,
                "password": payload.password,
                "birth_day": None,
                "country_code": None,

                # index_content
                "content_detail": None
            }

            __, result_personal_information = get_personal_information_by_email(email, db_session)
            if result_personal_information:
                return {"error_server": "00", "msg" : f"This {result_personal_information.email} is already a member."}

            result_user_profile = []
            timeout = time.time() + 4  # set timeout to 4 seconds
            while time.time() < timeout:
                profile_name_uuid = generator_uuid4()
                _, result_user_profile = get_user_profile_by_profile_name_uuid(profile_name_uuid, db_session)
                payload["profile_name_uuid"] = profile_name_uuid
                payload["username"] = email

                if result_user_profile == []:
                    break

                if time.time() > 2:
                    result = {"error_server": "01","msg": "Server is not ready, please try again."}
                    return result

            # Make sure profile_name_uuid
            if not profile_name_uuid:
                result = {"error_server": "02","msg": "Server is not ready, please try again."}
                return result
            
            item_user_profile = fill_create_user_profile(today, payload)
            db_session.add(item_user_profile)
            db_session.flush()

            item_personal_information = fill_create_personal_information(today, payload)
            db_session.add(item_personal_information)
            db_session.commit()
            redis_key = f"otp:{email}"
            redis_client.delete(redis_key)
            result = {"detail" : f"This {email} is successfully registered."}

    except Exception as e:
        logger.error(e)
        result = {"error_code": "03","msg": e}

    return result

def sending_mobile_sms_otp_by_mobile_phone_number(mobile_phone_number):
    result = None
    try:
        logger.debug(mobile_phone_number)
        if "+66" not in mobile_phone_number or len(mobile_phone_number) > 12:
            return {"error_code": "01","msg": "Invalid phone number request format : +66811111111"}

        result = sns.send_mobile_phone_number(mobile_phone_number)
        if "error_code" in result:
            return result
        elif "success_code" in result:
            result = {"detail" : result["msg"]}

    except Exception as e:
        logger.error(e)
        result = {"error_code": "02","msg": e}

    logger.debug(result)
    return result

def verify_mobile_sms_otp_by_mobile_phone_number(db_session, payload):
    result = None
    today = datetime.now()

    try:
        mobile_phone_number = payload.mobile_phone_number
        if "+66" not in mobile_phone_number or len(mobile_phone_number) > 12:
            return {"error_code": "01","msg": "Invalid phone number request format : +66811111111"}

        redis_client, result = ses.check_otp(mobile_phone_number, payload.otp_key)
        if "error_code" in result:
            return result
        elif "success_code" in result:
            payload = {
                # user_profile
                "profile_name_uuid": None,
                "profile_name": None,
                "images_profile_uuid": None,
                "username": None,
                "bio": None,
                "latitude": None,
                "longitude": None,
                "interests": None,
                "personal_information": None,
                "transaction_history": None,
                "social_graph": None,
                "clips_and_images": None,
                "message_chat": None,

                # personal_information
                "gender": None,
                "email": None,
                "mobile_phone_number": mobile_phone_number,
                "password": payload.password,
                "birth_day": None,
                "country_code": None,

                # index_content
                "content_detail": None
            }

            __, result_personal_information = get_personal_information_by_mobile_phone_number(mobile_phone_number, db_session)
            if result_personal_information:
                return {"error_server": "00", "msg" : f"This {result_personal_information.mobile_phone_number} is already a member."}

            result_user_profile = []
            timeout = time.time() + 4  # set timeout to 3 seconds
            while time.time() < timeout:
                profile_name_uuid = generator_uuid4()
                _, result_user_profile = get_user_profile_by_profile_name_uuid(profile_name_uuid, db_session)
                payload["profile_name_uuid"] = profile_name_uuid
                payload["username"] = mobile_phone_number

                if result_user_profile == []:
                    break

                if time.time() > 2:
                    result = {"error_server": "01","msg": "Server is not ready, please try again."}
                    return result

            # Make sure profile_name_uuid
            if not profile_name_uuid:
                result = {"error_server": "02","msg": "Server is not ready, please try again."}
                return result
            
            item_user_profile = fill_create_user_profile(today, payload)
            db_session.add(item_user_profile)
            db_session.flush()

            item_personal_information = fill_create_personal_information(today, payload)
            db_session.add(item_personal_information)
            db_session.commit()
            redis_key = f"otp:{mobile_phone_number}"
            redis_client.delete(redis_key)
            result = {"detail" : f"This {mobile_phone_number} is successfully registered."}

    except Exception as e:
        logger.error(e)
        result = {"error_code": "03","msg": e}

    return result



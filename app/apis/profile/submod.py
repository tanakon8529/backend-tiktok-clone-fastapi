from __future__ import annotations

from loguru import logger
from datetime import datetime, timedelta

from app.utilities.database_postgres.personal_information import login_personal_information_by_email, login_personal_information_by_mobile_phone_number
from app.utilities.database_postgres.user_profile import login_user_profile_by_cookie_cache_key, stamp_cookie_cache_key, get_user_profile_by_profile_name_uuid
from app.utilities.database_postgres.clips_profile import get_clips_profile_by_profile_name_uuid
from app.utilities.database_postgres.images_profile import get_images_profile_by_images_profile_uuid
from app.utilities.database_postgres.follower import get_follower_total
from app.utilities.database_postgres.following import get_following_total
from app.utilities.uuid_util import encode_cookie, decode_cookie 
from app.utilities.clip_content import generate_feed_details

from app.utilities.amazon.ses_util import ses_control
ses = ses_control()

from app.utilities.amazon.sns_util import sns_control
sns = sns_control()

def get_login_profile_by_mail(db_session, payload):
    logger.debug(payload)

    try:
        result = None
        _, result_personal_information = login_personal_information_by_email(payload, db_session)
        if not result_personal_information:
            return {"error_code": "01","msg": "Wrong email or password"}

        if (not payload.otp_key) and result_personal_information:
            return {"detail : email and password correct"}

        profile_name_uuid = result_personal_information.profile_name_uuid
        email = result_personal_information.email

        redis_client, result = ses.check_otp(email, payload.otp_key)
        if "error_code" in result:
            return result 

        cookie_cache_key = encode_cookie(email, payload.ip_address)
        session_user_profile, result_user_profile = get_user_profile_by_profile_name_uuid(profile_name_uuid, db_session)

        today = datetime.now()
        stamp_cookie_cache_key(today, session_user_profile, cookie_cache_key, db_session)

        session_user_profile, result_user_profile = get_user_profile_by_profile_name_uuid(profile_name_uuid, db_session)
        profile_name_uuid = result_user_profile.profile_name_uuid
        _, result_image_url_profile = get_images_profile_by_images_profile_uuid(result_user_profile.images_profile_uuid, db_session)
        _, result_following_total = get_following_total(profile_name_uuid, db_session)
        _, result_followers_total = get_follower_total(profile_name_uuid, db_session)
        _, result_clips_profile = get_clips_profile_by_profile_name_uuid(profile_name_uuid, db_session)

        db_session.commit()
        redis_key = f"otp:{email}"
        redis_client.delete(redis_key)

        profile_contents = None
        if result_clips_profile:
            profile_contents = generate_feed_details(result_clips_profile, db_session)

        result = {
            "detail" : f"{email} : Login success",
            "content" : "",
            "cookie_cache_key": result_user_profile.cookie_cache_key,
            "profile_name_uuid" : profile_name_uuid,
            "profile_name" : result_user_profile.profile_name,
            "profile_url" : result_image_url_profile.file_url_s3,
            "username" : result_user_profile.username,
            "following" : result_following_total,
            "followers" : result_followers_total,
            "likes" : 99,
            "profile_contents" : profile_contents
        }

    except Exception as e:
        logger.error(e)
        result = {"error_code": "02","msg": e}

    return result

def get_login_profile_by_mobile(db_session, payload):
    logger.debug(payload)

    try:
        result = None
        _, result_personal_information = login_personal_information_by_mobile_phone_number(payload, db_session)
        if result_personal_information == []:
            return {"error_code": "01","msg": "Wrong mobile phone number or password"}

        if (not payload.otp_key) and result_personal_information:
            return {"detail : mobile_phone_number and password correct"}

        profile_name_uuid = result_personal_information.profile_name_uuid
        mobile = result_personal_information.mobile_phone_number

        redis_client, result = ses.check_otp(mobile, payload.otp_key)
        if "error_code" in result:
            return result 
            
        cookie_cache_key = encode_cookie(mobile, payload.ip_address)
        session_user_profile, result_user_profile = get_user_profile_by_profile_name_uuid(profile_name_uuid, db_session)

        today = datetime.now()
        stamp_cookie_cache_key(today, session_user_profile, cookie_cache_key, db_session)

        session_user_profile, result_user_profile = get_user_profile_by_profile_name_uuid(profile_name_uuid, db_session)

        profile_name_uuid = result_user_profile.profile_name_uuid
        _, result_image_url_profile = get_images_profile_by_images_profile_uuid(result_user_profile.images_profile_uuid, db_session)
        _, result_following_total = get_following_total(profile_name_uuid, db_session)
        _, result_followers_total = get_follower_total(profile_name_uuid, db_session)
        _, result_clips_profile = get_clips_profile_by_profile_name_uuid(profile_name_uuid, db_session)

        db_session.commit()
        redis_key = f"otp:{mobile}"
        redis_client.delete(redis_key)

        profile_contents = None
        if result_clips_profile:
            profile_contents = generate_feed_details(result_clips_profile, db_session)

        result = {
            "detail" : f"{mobile} : Login success",
            "content" : "",
            "cookie_cache_key": result_user_profile.cookie_cache_key,
            "profile_name_uuid" : profile_name_uuid,
            "profile_name" : result_user_profile.profile_name,
            "profile_url" : result_image_url_profile.file_url_s3,
            "username" : result_user_profile.username,
            "following" : result_following_total,
            "followers" : result_followers_total,
            "likes" : 99,
            "profile_contents" : profile_contents
        }

    except Exception as e:
        logger.error(e)
        result = {"error_code": "02","msg": e}

    return result

def get_login_profile_by_key(db_session, payload):
    logger.debug(payload)

    try:
        result = None

        # Check User Cookile
        check_cookie = decode_cookie(payload.cookie_cache_key)
        if not check_cookie:
            return {"error_code": "01","msg": "Access Denied"}

        ip_address_in_key = check_cookie["ip_address"]
        user_login = check_cookie["user_login"]
        stamp_time_in_key = check_cookie["stamp_time"]
        
        # Valid Device
        if ip_address_in_key != payload.ip_address:
            return {"error_code": "02","msg": "Access Denied"}

        # Query Cookie in system
        _, result_user_profile = login_user_profile_by_cookie_cache_key(payload.cookie_cache_key, db_session)
        if not result_user_profile:
            return {"error_code": "03","msg": "Access Denied"}
        
        profile_name_uuid = result_user_profile.profile_name_uuid
        _, result_image_url_profile = get_images_profile_by_images_profile_uuid(result_user_profile.images_profile_uuid, db_session)
        _, result_following_total = get_following_total(profile_name_uuid, db_session)
        _, result_followers_total = get_follower_total(profile_name_uuid, db_session)
        _, result_clips_profile = get_clips_profile_by_profile_name_uuid(profile_name_uuid, db_session)

        # Expired in 90 days
        stamp_datetime = datetime.strptime(stamp_time_in_key, "%d-%m-%Y")
        now_datetime = datetime.now()
        time_diff = now_datetime - stamp_datetime
        if time_diff >= timedelta(days=90):
            return {"error_code": "04","msg": "Expired login session"}
        
        profile_contents = None
        if result_clips_profile:
            profile_contents = generate_feed_details(result_clips_profile, db_session)
        
        result = {
            "detail" : f"{user_login} : Login success",
            "content" : "",
            "cookie_cache_key": result_user_profile.cookie_cache_key,
            "profile_name_uuid" : profile_name_uuid,
            "profile_name" : result_user_profile.profile_name,
            "profile_url" : result_image_url_profile.file_url_s3,
            "username" : result_user_profile.username,
            "following" : result_following_total,
            "followers" : result_followers_total,
            "likes" : 99,
            "profile_contents" : profile_contents
        }

    except Exception as e:
        logger.error(e)
        result = {"error_code": "05","msg": e}

    return result


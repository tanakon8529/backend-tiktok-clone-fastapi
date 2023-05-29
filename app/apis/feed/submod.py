from __future__ import annotations

from loguru import logger

from app.utilities.database_postgres.clips_profile import get_clips_profile_random, get_clips_profile_by_profile_name_uuid
from app.utilities.database_postgres.user_profile import login_user_profile_by_cookie_cache_key
from app.utilities.clip_content import generate_feed_details

def get_init_feed_by_payload(payload, db_session):
    logger.debug(payload)

    cookie_cache_key = payload.get("cookie_cache_key")
    result = {"error_code": "01", "msg": "No data"}
    if cookie_cache_key:
        try:
            _, result_user_profile = login_user_profile_by_cookie_cache_key(cookie_cache_key, db_session)
            _, result_clips_profile = get_clips_profile_by_profile_name_uuid(result_user_profile.profile_name_uuid, db_session)

            if result_clips_profile:
                result = generate_feed_details(result_clips_profile, db_session)
        
        except Exception as e:
            logger.error(e)
            result = {"error_code": "02", "msg": f"Error retrieving data: {str(e)}"}

    else:
        try:
            _, result_clips_profile = get_clips_profile_random(db_session)

            if result_clips_profile:
                result = generate_feed_details(result_clips_profile, db_session)
        
        except Exception as e:
            logger.error(e)
            result = {"error_code": "03", "msg": f"Error retrieving data: {str(e)}"}

    return result



##### FOR TEST #####
# result = {
#             "feed": [
#                 {
#                     "index" : 0,
#                     "username": "@matheuscastroweb",
#                     "tags": "#testvideo #reactnative #tiktok #git #development #github #clone #react",
#                     "music": "Introducing Chromecast. The easiest way to enjoy",
#                     "likes": 94440,
#                     "total_comments": 6340,
#                     "uri": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
#                     "comments" : [
#                         {
#                             "id" : 0,
#                             "username"  : "แมวกระโดด8เมตร",
#                             "commecnt_time" : "22h",
#                             "text" : "How neatly i write the date in my book",
#                             "likes" : 123,
#                             "comments": [
#                                 {
#                                     "id" : 0,
#                                     "username"  : "แมวกระโดด8เมตร",
#                                     "commecnt_time" : "22h",
#                                     "text" : "How neatly i write the date in my book",
#                                     "likes" : 123,
#                                 },
#                                 {
#                                     "id" : 1,
#                                     "username"  : "แมวกระโดด8เมตร",
#                                     "commecnt_time" : "22h",
#                                     "text" : "How neatly i write the date in my book",
#                                     "likes" : 123,
#                                 }
#                             ]
#                         },
#                         {
#                             "id" : 1,
#                             "username"  : "แมวกระโดด8เมตร",
#                             "commecnt_time" : "22h",
#                             "text" : "How neatly i write the date in my book",
#                             "likes" : 123,
#                             "comments": [
#                                 {
#                                     "id" : 0,
#                                     "username"  : "แมวกระโดด8เมตร",
#                                     "commecnt_time" : "22h",
#                                     "text" : "How neatly i write the date in my book",
#                                     "likes" : 123,
#                                 },
#                                 {
#                                     "id" : 1,
#                                     "username"  : "แมวกระโดด8เมตร",
#                                     "commecnt_time" : "22h",
#                                     "text" : "How neatly i write the date in my book",
#                                     "likes" : 123,
#                                 }
#                             ]
#                         }
#                     ]
#                 },
#                 {
#                     "index" : 1,
#                     "username": "@dedeedevteams",
#                     "tags": "#testvideo #reactnative #tiktok #git #development #github #clone #react",
#                     "music": "Introducing Chromecast. The easiest way to enjoy",
#                     "likes": 52366,
#                     "total_comments": 1621,
#                     "uri": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
#                     "comments" : [
#                         {
#                             "id" : 0,
#                             "username"  : "แมวกระโดด8เมตร",
#                             "commecnt_time" : "22h",
#                             "text" : "How neatly i write the date in my book",
#                             "likes" : 123,
#                             "comments": [
#                                 {
#                                     "id" : 0,
#                                     "username"  : "แมวกระโดด8เมตร",
#                                     "commecnt_time" : "22h",
#                                     "text" : "How neatly i write the date in my book",
#                                     "likes" : 123,
#                                 },
#                                 {
#                                     "id" : 1,
#                                     "username"  : "แมวกระโดด8เมตร",
#                                     "commecnt_time" : "22h",
#                                     "text" : "How neatly i write the date in my book",
#                                     "likes" : 123,
#                                 }
#                             ]
#                         },
#                         {
#                             "id" : 1,
#                             "username"  : "แมวกระโดด8เมตร",
#                             "commecnt_time" : "22h",
#                             "text" : "How neatly i write the date in my book",
#                             "likes" : 123,
#                             "comments": [
#                                 {
#                                     "id" : 0,
#                                     "username"  : "แมวกระโดด8เมตร",
#                                     "commecnt_time" : "22h",
#                                     "text" : "How neatly i write the date in my book",
#                                     "likes" : 123,
#                                 },
#                                 {
#                                     "id" : 1,
#                                     "username"  : "แมวกระโดด8เมตร",
#                                     "commecnt_time" : "22h",
#                                     "text" : "How neatly i write the date in my book",
#                                     "likes" : 123,
#                                 }
#                             ]
#                         }
#                     ]
#                 },
#             ]
#         }
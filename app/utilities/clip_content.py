from app.utilities.database_postgres.user_profile import  get_user_profile_by_profile_name_uuid
from app.utilities.database_postgres.user_activity import get_user_activity_by_clips_group_uuid
from loguru import logger
from typing import Dict, List, Optional
from datetime import datetime

MAX_FEED_LENGTH = 10

def initialize_feed_item():
    return {
        "index": 0,
        "username": None,
        "tags": None,
        "music": None,
        "likes": None,
        "total_comments": None,
        "uri": None,
        "comments": None
    }

def get_comments_tree(comments):
    comments_tree = []
    for comment in comments:
        comment_tree = {
            "id": comment.id,
            "username": comment.username,
            "comment_time": comment.comment_time.strftime("%Y-%m-%d %H:%M:%S"),
            "text": comment.text,
            "likes": comment.likes,
            "comments": []
        }
        if comment.replies:
            comment_tree["comments"] = get_comments_tree(comment.replies)
        comments_tree.append(comment_tree)
    return comments_tree

def generate_feed_details(result_clips_profile, db_session):
    result_format = {"feed": []}
    for index, clip in enumerate(result_clips_profile):
        feed_item = initialize_feed_item()
        feed_item["index"] = index

        _, result_user_profile_by_clip = get_user_profile_by_profile_name_uuid(clip.profile_name_uuid, db_session)
        if result_user_profile_by_clip:
            feed_item["username"] = result_user_profile_by_clip.username

        _, result_user_activity = get_user_activity_by_clips_group_uuid(clip.clips_profile_uuid, db_session)
        if result_user_activity:
            feed_item["tags"] = result_user_activity.content
            feed_item["likes"] = result_user_activity.likes

        feed_item["uri"] = clip.file_url_s3

        # comments = get_comments_tree(clip.comments)
        # feed_item["total_comments"] = len(comments)
        # feed_item["comments"] = comments

        result_format["feed"].append(feed_item)
        if len(result_format["feed"]) == MAX_FEED_LENGTH:
            break
    logger.debug(f"Generated {len(result_format['feed'])} feed items")
    return result_format

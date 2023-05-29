from sqlalchemy import or_, and_
from loguru import logger

from app.core.db_model import Follower
from app.apis.clients.model import follower_base_model

def get_follower_total(profile_name_uuid, db_session):
    session_follower = db_session.query(Follower).filter(Follower.profile_name_uuid==profile_name_uuid).order_by(Follower.create_date.desc()).all()
    result_follower = []
    for i in session_follower:
        x = follower_base_model(**i.__dict__)
        result_follower.append(x)

    return session_follower, result_follower

def get_follower_by_profile_name_uuid(profile_name_uuid, db_session):
    session_follower = db_session.query(Follower).filter(Follower.profile_name_uuid==profile_name_uuid)
    result_follower = []
    for i in session_follower:
        x = follower_base_model(**i.__dict__)
        result_follower.append(x)

    if result_follower:
        result_follower = result_follower[0]
    return session_follower, result_follower

def fill_create_follower(today, payload):
    
    item_follower = Follower(
        profile_name_uuid = payload["profile_name_uuid"],
        follower_profile_uuid = payload["follower_profile_uuid"],
        create_date = today
    )

    return item_follower
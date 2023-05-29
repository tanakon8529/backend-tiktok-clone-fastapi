from sqlalchemy import or_, and_
from loguru import logger

from app.core.db_model import PersonalInformation
from app.apis.clients.model import personal_information_base_model

def login_personal_information_by_email(payload, db_session):
    session_personal_information = db_session.query(PersonalInformation).filter(and_(PersonalInformation.email==payload.email), (PersonalInformation.password==payload.password))
    result_personal_information = []
    for i in session_personal_information:
        x = personal_information_base_model(**i.__dict__)
        result_personal_information.append(x)

    if result_personal_information:
        result_personal_information = result_personal_information[0]
    return session_personal_information, result_personal_information

def login_personal_information_by_mobile_phone_number(payload, db_session):
    session_personal_information = db_session.query(PersonalInformation).filter(and_(PersonalInformation.mobile_phone_number==payload.mobile_phone_number), (PersonalInformation.password==payload.password))
    result_personal_information = []
    for i in session_personal_information:
        x = personal_information_base_model(**i.__dict__)
        result_personal_information.append(x)
        
    if result_personal_information:
        result_personal_information = result_personal_information[0]
    return session_personal_information, result_personal_information

def get_personal_information_by_mobile_phone_number(mobile_phone_number, db_session):
    session_personal_information = db_session.query(PersonalInformation).filter(PersonalInformation.mobile_phone_number==mobile_phone_number)
    result_personal_information = []
    for i in session_personal_information:
        x = personal_information_base_model(**i.__dict__)
        result_personal_information.append(x)

    if result_personal_information:
        result_personal_information = result_personal_information[0]
    return session_personal_information, result_personal_information


def get_personal_information_by_email(email, db_session):
    session_personal_information = db_session.query(PersonalInformation).filter(PersonalInformation.email==email)
    result_personal_information = []
    for i in session_personal_information:
        x = personal_information_base_model(**i.__dict__)
        result_personal_information.append(x)

    if result_personal_information:
        result_personal_information = result_personal_information[0]
    return session_personal_information, result_personal_information


def fill_create_personal_information(today, payload):
    
    item_personal_information = PersonalInformation(
        create_date = today,
        modified_date = today,
        profile_name_uuid = payload["profile_name_uuid"],
        gender = payload["gender"],
        email = payload["email"],
        mobile_phone_number = payload["mobile_phone_number"],
        password = payload["password"],
        birth_day = payload["birth_day"],
        country_code = payload["country_code"]
    )

    return item_personal_information

def edit_personal_information(today, personal_information, payload, db_session):
    data_updates = {
        "modified_date": today,
        "gender": payload["gender"],
        "email": payload["email"],
        "mobile_phone_number": payload["mobile_phone_number"],
        "birth_day": payload["birth_day"],
        "country_code": payload["country_code"],
        "password": payload["password"],
    }

    personal_information.update(data_updates)
    db_session.flush()
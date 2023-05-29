from sqlalchemy import or_, and_
from loguru import logger

from app.core.db_model import Countries
from app.apis.masters.model import countries_ModelBase

def get_countries_all(db_session):
    session_countries = db_session.query(Countries).all()
    result_countries = []
    for i in session_countries:
        x = countries_ModelBase(**i.__dict__)
        result_countries.append(x)

    return session_countries, result_countries
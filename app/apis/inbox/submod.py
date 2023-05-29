from __future__ import annotations

from loguru import logger

from app.utilities.database_postgres.countries import get_countries_all

def get_all_countries_from_pg(db_session):
    session_countries, result_countries = get_countries_all(db_session)
    try:
        if not result_countries:
            result_countries = {"error_code": "01","msg": "Not found countries"}

        return result_countries
    except Exception as e:
        logger.error(e)
        result_document = {"error_code": "02","msg": e}

    return result_document

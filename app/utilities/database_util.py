from app.settings.configs import DATABASE_NAME, DATABASE_SERVER, DATABASE_USERNAME, DATABASE_PASSWORD
import urllib.parse

def url_database():
    database_name = DATABASE_NAME
    database_server = DATABASE_SERVER
    database_username = DATABASE_USERNAME
    # password "@" in string
    database_password = urllib.parse.quote_plus(DATABASE_PASSWORD)
    quote_db = f"postgresql+psycopg2://{database_username}:{database_password}@{database_server}:5432/{database_name}"

    return quote_db
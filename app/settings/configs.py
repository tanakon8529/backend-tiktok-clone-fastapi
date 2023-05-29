import os
from dotenv import load_dotenv

load_dotenv("./.env")

# API
API_VERSION = os.environ["API_VERSION"]
API_PATH = os.environ["API_PATH"]
API_DOC = os.environ["API_DOC"]
HOST = os.environ["HOST"]
PORT = os.environ["PORT"]
SERVER_ROLE = os.environ["SERVER_ROLE"]

#### AWS ####
AWS_KEY_ID = os.environ["AWS_KEY_ID"]
AWS_KEY_SECRET = os.environ["AWS_KEY_SECRET"]
AWS_REGION = os.environ["AWS_REGION"]

BUCKET_NAME_SYSTEM = os.environ["BUCKET_NAME_SYSTEM"]
BUCKET_NAME_CLIENT_IMAGES = os.environ["BUCKET_NAME_CLIENT_IMAGES"]
BUCKET_NAME_CLIENT_CLIPS = os.environ["BUCKET_NAME_CLIENT_CLIPS"]

SES_NAME = os.environ["SES_NAME"]
SES_USERNAME = os.environ["SES_USERNAME"]
SES_PASSWORD = os.environ["SES_PASSWORD"]
SES_ENDPOINT =  os.environ["SES_ENDPOINT"]
CF_EMAIL_SENDER = os.environ["CF_EMAIL_SENDER"]

SNS_ACCESS_KEY =  os.environ["SNS_ACCESS_KEY"]
SNS_SECRET_KEY =  os.environ["SNS_SECRET_KEY"]

#### DATABASE ####
DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_SERVER = os.environ["DATABASE_SERVER"]
DATABASE_USERNAME = os.environ["DATABASE_USERNAME"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_PORT = os.environ["DATABASE_PORT"]
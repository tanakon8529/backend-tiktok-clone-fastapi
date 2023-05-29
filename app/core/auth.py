from datetime import timedelta
from uuid import uuid4
from loguru import logger
from fastapi import Header, HTTPException

from app.utilities.redis import get_primary_client

# Define token expiration time (in minutes)
token_expire_minutes = 60

username_pack = ["dedee.dev.001@developer.com",
                 "dedee.dev.002@developer.com"
                 ]

password_pack = ["nx<8z;pyAw-S[MG^/`v5NdJBj+h>b}]V",
                 "v`M'74Lk(;bduFjr<eX&ChQ#*6cw3z_]"
                 ]

# for other /access/protected
def valid_access_token(token: str = Header(...)):
    if "Dedee_Bearer" in token:
        token = token.replace("Dedee_Bearer", "").replace(" ", "")
    else:
        raise HTTPException(status_code=401, detail='Invalid access token')

    # Check if access token is valid
    redis = get_primary_client()
    token_key = f'token:{token}'
    if not redis.get(token_key):
        raise HTTPException(status_code=401, detail='Invalid access token')

    return {'detail': 'Valid access token!'}

# Authenticate user and return access token
def authenticate_user(username: str, password: str):
    # Replace this with your own authentication logic
    access_token = None
    if username in username_pack and password in password_pack:
        access_token = str(uuid4())

    return access_token

# Store access token in Redis and return token info
def store_access_token(access_token: str):
    try:
        # Generate token key
        token_key = f'token:{access_token}'
        # Store access token with expiration time
        redis = get_primary_client()
        redis.setex(token_key, timedelta(minutes=token_expire_minutes), access_token)
        # Return token info
        result = {'access_token': access_token, 'token_type': 'Dedee_Bearer'}
    except Exception as e:
        logger.error(e)
        result = e

    return result
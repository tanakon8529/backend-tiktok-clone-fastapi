import uuid
import jwt
import json

from datetime import datetime

def generator_uuid4():
    gen_uuid =str(uuid.uuid4())
    return gen_uuid


def encode_cookie(user_login, ip_address):
    today = datetime.now().strftime('%d-%m-%Y')

    message = {
        "stamp_time" : today,
        "user_login" : user_login,
        "ip_address" : ip_address
    }
    en_mess = json.dumps(message)
    key_jwt = "R7VFSjg/d!Kzx6D$U}Aw*?~qk4Pt9@y"
    key_encode = jwt.encode({"cookie": en_mess}, key_jwt, algorithm="HS256")
    return key_encode


def decode_cookie(key_encode):
    key_jwt = "R7VFSjg/d!Kzx6D$U}Aw*?~qk4Pt9@y"
    res_decode = jwt.decode(key_encode, key_jwt, algorithms=["HS256"])
    cookie_user = json.loads(res_decode["cookie"])
    return cookie_user


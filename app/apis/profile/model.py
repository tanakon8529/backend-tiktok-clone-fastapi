from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

########## Model Login ##########
#########################################
class login_mail_model(BaseModel):
    email : str
    password : str
    otp_key : str = None
    ip_address : str

class login_mobile_model(BaseModel):
    mobile_phone_number : str
    password : str
    otp_key : str = None
    ip_address : str

class cookie_cache_key_model(BaseModel):
    cookie_cache_key : str
    ip_address : str

#########################################
#########################################
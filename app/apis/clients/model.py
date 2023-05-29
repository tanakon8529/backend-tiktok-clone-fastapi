from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

########## Model mail & sms otp ##########
###############################
class verify_mail_otp_model(BaseModel):
    email: str = None
    password : str = None
    otp_key: str = None

class verify_sms_otp_model(BaseModel):
    mobile_phone_number: str = None
    password : str = None
    otp_key: str = None

###############################
###############################


########## Model query ##########
#################################
class user_profile_base_model(BaseModel):
    profile_name_uuid: str
    profile_name: str
    images_profile_uuid: str
    username: str = None
    bio: str = None
    latitude: str = None
    longitude: str = None
    interests: str = None
    create_date: datetime
    modified_date: datetime
    cookie_cache_key: str = None

class images_profile_base_model(BaseModel):
    images_profile_uuid: str
    create_date: datetime
    modified_date: datetime
    profile_name_uuid: str
    file_name: str = None
    file_type: str = None
    file_size_kb: int = None
    file_key_s3: str = None
    file_url_s3: str = None
    file_url_expire_date_s3: datetime

class clips_profile_base_model(BaseModel):
    clips_profile_uuid: str
    create_date: datetime
    modified_date: datetime
    profile_name_uuid: str
    file_name: str = None
    file_type: str = None
    file_size_kb: int = None
    file_key_s3: str = None
    file_url_s3: str = None
    file_url_expire_date_s3: datetime

class images_group_base_model(BaseModel):
    images_profile_uuid: str
    create_date: datetime
    modified_date: datetime
    profile_name_uuid: str
    file_name: str = None
    file_type: str = None
    file_size_kb: int = None
    file_key_s3: str = None
    file_url_s3: str = None
    file_url_expire_date_s3: datetime

class clips_group_base_model(BaseModel):
    clips_group_uuid: str
    create_date: datetime
    modified_date: datetime
    profile_name_uuid: str
    file_name: str = None
    file_type: str = None
    file_size_kb: int = None
    file_key_s3: str = None
    file_url_s3: str = None
    file_url_expire_date_s3: datetime

class personal_information_base_model(BaseModel):
    create_date: datetime
    modified_date: datetime
    profile_name_uuid: str = None
    gender: str = None
    email: str = None
    mobile_phone_number: str = None
    birth_day: str = None
    country_code: str = None

class index_content_base_model(BaseModel):
    profile_name_uuid: str
    create_date: datetime
    modified_date: datetime
    content_detail: dict = None

class follower_base_model(BaseModel):
    profile_name_uuid: str
    follwer_profile_uuid: str
    create_date: datetime

class following_base_model(BaseModel):
    profile_name_uuid: str
    following_profile_uuid: str
    create_date: datetime

class user_activity_base_model(BaseModel):
    user_activity_uuid: str
    profile_name_uuid: str
    create_date: datetime
    modified_date: datetime
    content: str = None
    likes: int = None
    clips_group_uuid: str = None
    images_group_uuid: str = None

###############################
###############################


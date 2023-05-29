from datetime import datetime
from pydantic import BaseModel

import json

########## Model app/core/db_model ##########
#############################################

class clips_profile_base_model(BaseModel):
    clips_profile_uuid: str
    create_date: datetime
    modified_date: datetime
    profile_name_uuid: str = None
    file_name: str = None
    file_type: str = None
    file_size_kb: int = None
    file_key_s3: str = None
    file_url_s3: str = None
    file_url_expire_date_s3: datetime = None

class clips_group_base_model(BaseModel):
    clips_group_uuid: str
    create_date: datetime
    modified_date: datetime
    profile_name_uuid: str = None
    file_name: str = None
    file_type: str = None
    file_size_kb: int = None
    file_key_s3: str = None
    file_url_s3: str = None
    file_url_expire_date_s3: datetime = None

class images_profile_base_model(BaseModel):
    images_profile_uuid: str
    create_date: datetime
    modified_date: datetime
    profile_name_uuid: str = None
    file_name: str = None
    file_type: str = None
    file_size_kb: int = None
    file_key_s3: str = None
    file_url_s3: str = None
    file_url_expire_date_s3: datetime = None

class images_group_base_model(BaseModel):
    images_group_uuid: str
    create_date: datetime
    modified_date: datetime
    profile_name_uuid: str = None
    file_name: str = None
    file_type: str = None
    file_size_kb: int = None
    file_key_s3: str = None
    file_url_s3: str = None
    file_url_expire_date_s3: datetime = None

#########################################
#########################################

########### Model On Create #############
#########################################

class UploadFileBase(BaseModel):
    profile_name_uuid : str
    uploadtype : str = "images or clips"
    file_type: str = None

    # https://stackoverflow.com/questions/65504438/how-to-add-both-file-and-json-body-in-a-fastapi-post-request
    # Method 4
    # A likely preferable method comes from the discussion here, and incorporates a custom class with
    # a classmethod used to transform a given JSON string into a Python dictionary, which is then used 
    # for validation against the Pydantic model. Similar to Method 3 above, the input data should be 
    # passed as a single Form parameter in the form of JSON string. Thus, the same test.py file(s) and 
    # index.html template from the previous method can be used for testing the below.
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

########### Model On delete (for front-end sending) #############
#################################################################

class Delete_Model(BaseModel):
    images_profile_uuid: str = None
    images_group_uuid: str = None
    clips_group_uuid: str = None
    clips_profile_uuid: str = None
    file_name: str = None
    file_key_s3: str

class Delete_Pack_Model(BaseModel):
    uploadtype: str = "images_profile or images_group or clips_group or clips_profile"
    details_delete: list[Delete_Model]

#########################################
#########################################
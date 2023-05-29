from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

########## Model Query ##########
#########################################
class countries_ModelBase(BaseModel):
    country_code : str = None
    create_date : datetime = None
    modified_date : datetime = None
    country_name : str = None

#########################################
#########################################
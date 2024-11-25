from pydantic import BaseModel
from pydantic import StringConstraints
from typing import Annotated,Literal


class AWSConfig(BaseModel):
    aws_access_key_id:str
    aws_secret_access_key:str
    endpoint_url:str
    region_name:str
    verify:bool

from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,GetManySchema
from typing import List,Optional,Dict,Any,Literal,Union
from datetime import datetime,date
from pydantic import BaseModel,StringConstraints
from typing_extensions import Annotated

class LoginSchema(BaseSchema):
    username:Annotated[str,StringConstraints()]
    password:Annotated[str,StringConstraints()]

class TokenSchema(BaseSchema):
    access_token:str
    token_type:str

class TokenResponseSchema(BaseResponseSchema):
    data:TokenSchema

class UserSessionIdentifier(BaseModel):
    user_id:str
    username:str
    email:str



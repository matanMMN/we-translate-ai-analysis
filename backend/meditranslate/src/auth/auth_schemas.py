from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,GetManySchema,UserNameStr,PassWordStr,NameStr
from typing import List,Optional,Dict,Any,Literal,Union
from datetime import datetime,date
from pydantic import BaseModel, EmailStr, Field,StringConstraints
from typing_extensions import Annotated

AccessTokenStr = Annotated[str,StringConstraints()]
TokenTypeStr =  Annotated[str,StringConstraints()] #Literal['Bearer']

class LoginSchema(BaseSchema):
    username:UserNameStr = Field(..., title="Email", description="User email address")
    password:PassWordStr = Field(..., title="Email", description="User email address")

class TokenSchema(BaseSchema):
    access_token:AccessTokenStr = Field(..., title="Email", description="User email address")
    token_type:TokenTypeStr = Field(..., title="Email", description="User email address")

class RegisterUserSchema(BaseSchema):
    email : EmailStr = Field(..., title="Email", description="User email address")
    username :UserNameStr = Field(..., title="Username", description="User's username")
    password : PassWordStr = Field(..., title="Password", description="Password")
    first_name : Optional[NameStr] = Field(None, title="firstname", description="")
    last_name : Optional[NameStr] = Field(None, title="lastname", description="")


class TokenResponseSchema(BaseResponseSchema):
    data:TokenSchema

from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,GetManySchema,UserNameStr,PassWordStr,NameStr
from typing import List,Optional,Dict,Any,Literal,Union
from datetime import datetime,date
from pydantic import BaseModel, EmailStr, Field,StringConstraints
from typing_extensions import Annotated
from meditranslate.utils.user_role.user_role import UserRole

AccessTokenStr = Annotated[str,StringConstraints()]
TokenTypeStr =  Annotated[str,StringConstraints()] #Literal['Bearer']

class LoginSchema(BaseSchema):
    username:UserNameStr = Field(..., title="Email", description="User Email address")
    password:PassWordStr = Field(..., title="Password", description="User Password")

class TokenSchema(BaseSchema):
    access_token:AccessTokenStr = Field(..., title="Email", description="User email address")
    token_type:TokenTypeStr = Field(..., title="Token Type", description="Bearer")

class RegisterUserSchema(BaseSchema):
    email : EmailStr = Field(..., title="Email", description="User Email address")
    username :UserNameStr = Field(..., title="Username", description="Username")
    password : PassWordStr = Field(..., title="Password", description="Password")
    first_name : Optional[NameStr] = Field(None, title="firstname", description="")
    last_name : Optional[NameStr] = Field(None, title="lastname", description="")
    role : Optional[str] = Field(UserRole.TRANSLATOR, title="role", description="")


class TokenResponseSchema(BaseResponseSchema):
    data:TokenSchema

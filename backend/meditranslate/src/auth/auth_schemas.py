from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,GetManySchema
from typing import List,Optional,Dict,Any,Literal,Union
from datetime import datetime,date
from pydantic import BaseModel, EmailStr, Field,StringConstraints
from typing_extensions import Annotated

class LoginSchema(BaseSchema):
    username:Annotated[str,StringConstraints()]
    password:Annotated[str,StringConstraints()]

class TokenSchema(BaseModel):
    access_token:str
    token_type:str

class TokenResponseSchema(BaseResponseSchema):
    data:TokenSchema


class RegisterUserSchema(BaseModel):
    email : Annotated[
                    Optional[EmailStr],
                    StringConstraints(
                        strip_whitespace=True,
                        to_upper=None,
                        to_lower=None,
                        strict=None,
                        max_length=None,
                        min_length=None,
                        pattern=None,
                    ),
                ] = Field(None, title="Email", description="User email address")

    username : Annotated[
                    Optional[str],
                    StringConstraints(
                        strip_whitespace=True,
                        to_upper=None,
                        to_lower=None,
                        strict=None,
                        max_length=None,
                        min_length=None,
                        pattern=None,
                    ),
                ] = Field(None, title="Username", description="User's username")

    password : Annotated[
                    Optional[str],
                    StringConstraints(
                        strip_whitespace=True,
                        to_upper=None,
                        to_lower=None,
                        strict=None,
                        max_length=None,
                        min_length=None,
                        # pattern=r'^\+?[1-9]\d{1,14}$',
                    ),
                ] = Field(None, title="Password", description="Password")

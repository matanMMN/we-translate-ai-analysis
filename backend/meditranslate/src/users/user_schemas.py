from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,GetManySchema
from typing import List,Optional,Dict,Any,Literal,Union
from datetime import datetime,date
from pydantic import BaseModel, HttpUrl,constr,field_validator,Field,EmailStr,StringConstraints,ConfigDict
import re
from typing_extensions import Annotated


class BaseUserSchema(BaseSchema):
    model_config:ConfigDict=ConfigDict(
        extra="ignore",
        strict=False
    )
    id : Annotated[
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
                ] = Field(None, title="User ID", description="Unique identifier for the user")
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
                ] = Field(None, title="Password", description="Password",repr=False)


    first_name : Annotated[
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
                ] = Field(None, title="First Name", description="User's first name")

    last_name : Annotated[
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
                ] = Field(None, title="Last Name", description="User's last name")


    # user roles
    # roles : Optional[List[str]] = Field([], title="Roles", description="List of roles assigned to the user")
    # # roles : Optional[List[str]] = Field(None, title="Roles", description="List of roles assigned to the user")

    # additional_fields: Optional[Dict[str, Any]] = Field(None, title="Additional Fields", description="Any additional user data")
    # avatar: Optional[bytes] = Field(None, title="avatar", description="Any additional user data")
    # avatar_url:  Optional[str] = Field(None, title="avatar_url", description="Any additional user data")

    last_login: Optional[date] = Field(None, title="last_login", description="Any additional user data")
    # is_disabled: Optional[bool] = Field(None, title="is_disabled", description="Any additional user data")
    # is_deleted: Optional[bool] = Field(None, title="is_deleted", description="Any additional user data")

    # # roles: Optional[List[Any]] = Field(None, title="roles", description="Any additional user data")

    created_by: Optional[str]  = Field(None, title="created_by", description="Any additional user data")
    updated_by: Optional[str]  = Field(None, title="updated_by", description="Any additional user data")


class UserCreateSchema(BaseUserSchema):
    pass

class UserUpdateSchema(BaseUserSchema):
    pass


class UserResponseSchema(BaseResponseSchema):
    data: BaseUserSchema

class UsersResponseSchema(BaseResponseSchema):
    data: List[BaseUserSchema]









# class UserRoleSchema(BaseModel):
#     role_id : Annotated[
#                     Optional[str],
#                     StringConstraints(
#                         strip_whitespace=True,
#                         to_upper=None,
#                         to_lower=None,
#                         strict=None,
#                         max_length=None,
#                         min_length=None,
#                         pattern=None,
#                     ),
#                 ] = Field(None, title="Role ID", description="Unique identifier for the role")

#     role_name : Annotated[
#                     Optional[str],
#                     StringConstraints(
#                         strip_whitespace=True,
#                         to_upper=None,
#                         to_lower=None,
#                         strict=None,
#                         max_length=None,
#                         min_length=None,
#                         pattern=None,
#                     ),
#                 ] = Field(None, title="Role Name", description="Name of the role")


# class UserAccessControlSchema(BaseModel):
#     roles : Annotated[
#                     Optional[List[UserRoleSchema]],
#                     StringConstraints(
#                         strip_whitespace=True,
#                         to_upper=None,
#                         to_lower=None,
#                         strict=None,
#                         max_length=None,
#                         min_length=None,
#                         pattern=None,
#                     ),
#                 ] = Field(None, title="Roles", description="List of roles assigned to the user")


from meditranslate.utils.user_role.user_role import UserRole
from meditranslate.app.shared.schemas import BaseResponseSchema, BaseSchema,GetManySchema,ObjectIdSchema,UserFullNamesModificationSchema, UserIdentifiersModificationSchema,ModificationTimestampSchema,NameStr,UserNameStr,PassWordStr
from typing import List,Optional,Dict,Any,Literal,Union
from datetime import datetime,date
from pydantic import BaseModel, HttpUrl,constr,field_validator,Field,EmailStr,StringConstraints,ConfigDict
import re
from typing_extensions import Annotated

class PublicUserSchema(ObjectIdSchema,UserFullNamesModificationSchema,ModificationTimestampSchema):
    email: EmailStr = Field(..., title="Email", description="User email address")
    first_name: Optional[NameStr] = Field(None, title="First Name", description="User's first name")
    last_name : Optional[NameStr]= Field(None, title="Last Name", description="User's last name")
    last_login: Optional[date] = Field(None, title="last_login", description="Any additional user data")
    role : Optional[str] = Field(UserRole.TRANSLATOR, title="role", description="")
class UserSchema(ObjectIdSchema,UserFullNamesModificationSchema,ModificationTimestampSchema,UserIdentifiersModificationSchema):
    email : EmailStr = Field(None, title="Email", description="User email address")
    username : UserNameStr = Field(None, title="Username", description="User's username")
    first_name : Optional[NameStr] = Field(None, title="First Name", description="User's first name")
    last_name : Optional[NameStr] = Field(None, title="Last Name", description="User's last name")
    last_login: Optional[date] = Field(None, title="last_login", description="Any additional user data")
    role : Optional[str] = Field(UserRole.TRANSLATOR, title="role", description="")
class UserCreateSchema(BaseSchema):
    email :EmailStr = Field(..., title="Email", description="User email address")
    username : UserNameStr = Field(..., title="Username", description="User's username")
    password : PassWordStr = Field(..., title="Password", description="Password",repr=False)
    first_name : NameStr = Field(None, title="First Name", description="User's first name")
    last_name : NameStr = Field(None, title="LaBaseUserSchema,Creast Name", description="User's last name")
    role : Optional[str] = Field(UserRole.TRANSLATOR, title="role", description="")

class UserUpdateSchema(BaseSchema):
    email : Optional[EmailStr] = Field(None, title="Email", description="User email address")
    username : Optional[UserNameStr]= Field(None, title="Username", description="User's username")
    password : Optional[PassWordStr] = Field(None, title="Password", description="Password",repr=False)
    first_name : Optional[NameStr] = Field(None, title="First Name", description="User's first name")
    last_name : Optional[NameStr] = Field(None, title="First Name", description="User's Last name")
    role : Optional[str] = Field(UserRole.TRANSLATOR, title="role", description="")

class UserResponseSchema(BaseResponseSchema):
    data: UserSchema

class UsersResponseSchema(BaseResponseSchema):
    data: List[UserSchema]

class PublicUserResponseSchema(BaseResponseSchema):
    data: PublicUserSchema

class PublicUsersResponseSchema(BaseResponseSchema):
    data: List[PublicUserSchema]










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


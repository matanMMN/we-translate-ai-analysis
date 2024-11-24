from pydantic import BaseModel
from meditranslate.app.shared.schemas import BaseSchema,GetManySchema,BaseResponseSchema
from typing import List,Optional,Dict,Any,Literal,Union
from datetime import datetime,date
from pydantic import BaseModel, HttpUrl,constr,field_validator,Field,StringConstraints
import re
import pycountry
import pytz
from typing_extensions import Annotated



class RoleCreateSchema(BaseSchema):
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
                ] = Field(None, title="role id", description="role's id")
    name : Annotated[
                    str,
                    StringConstraints(
                        strip_whitespace=True,
                        to_upper=None,
                        to_lower=None,
                        strict=None,
                        max_length=None,
                        min_length=None,
                        pattern=None,
                    ),
                ] = Field(title="Name", description="role's  name")
    description : Annotated[
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
                ] = Field(None, title="description", description="User's first name")
    users : Optional[List[str]] = Field([], title="users", description="List of roles assigned to the user")
    permissions: Optional[List[str]] = Field([], title="permissions", description="List of roles assigned to the user")
    parent_roles: Optional[List[str]] = Field([], title="parent roles", description="List of roles")
    child_roles: Optional[List[str]] = Field([], title="child roles", description="List of roles ")



class RoleUpdateSchema(BaseSchema):
    role_id : Annotated[
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
    name : Annotated[
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
    description : Annotated[
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
    permissions: Optional[List[str]] = Field([], title="Roles", description="List of roles assigned to the user")



class UserRoleCreateSchema(BaseSchema):
    role_id : Annotated[
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
    user_id : Annotated[
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

class RolePermissionCreateSchema(BaseSchema):
    role_id : Annotated[
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
    permission_id : Annotated[
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

class PermissionCreateSchema(BaseSchema):
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
                ] = Field(None, title="First Name", description="User's first name")

    action : Annotated[
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
    resource : Annotated[
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
    description : Annotated[
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

    roles: Optional[List[str]] = Field([], title="Roles", description="List of roles assigned to the user")

class PermissionUpdateSchema(BaseSchema):
    permission_id : Annotated[
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

    action : Annotated[
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
    resource : Annotated[
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
    description : Annotated[
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

    roles: Optional[List[str]] = Field([], title="Roles", description="List of roles assigned to the user")


class RoleHierarchyCreateSchema(BaseSchema):
    parent_role_id : Annotated[
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
    child_role_id : Annotated[
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


class RolesGetManySchema(GetManySchema):
    pass

class PermissionsGetManySchema(GetManySchema):
    pass


class RoleResponseSchema(BaseResponseSchema):
    pass

class RolesResponseSchema(BaseResponseSchema):
    pass

class PermissionResponseSchema(BaseResponseSchema):
    pass

class PermissionsResponseSchema(BaseResponseSchema):
    pass

class RoleHierarchyResponseSchema(BaseResponseSchema):
    pass

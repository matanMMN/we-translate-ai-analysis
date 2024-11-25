from meditranslate.src.access_control.access_control_schemas import (
    UserRoleCreateSchema,
    RolePermissionCreateSchema,
    PermissionCreateSchema,
    PermissionUpdateSchema,
    PermissionsGetManySchema,
    RoleHierarchyCreateSchema,
    RoleCreateSchema,
    RolesGetManySchema,
    RoleUpdateSchema
)
from meditranslate.src.access_control import access_control_service
from fastapi import Request
from typing import List,Optional,Dict,Any,Tuple

from meditranslate.app.db.models import (
    Permission,
    Role,
    RolePermission,
    UserRole
)


async def create_role(request:Request, role_create_schema:RoleCreateSchema, *args: Any,**kwargs: Any) -> Role:
    role_create = role_create_schema.model_dump() if role_create_schema else {}
    return await access_control_service.create_role(role_create, *args,**kwargs)

async def get_role(request:Request, role_id: str, *args:Any,**kwargs:Any) -> Role:
    return await access_control_service.get_role(role_id,*args,**kwargs)

async def update_role(request:Request, role_id: str, role_update_schema:RoleUpdateSchema, *args:Any,**kwargs:Any) -> Role:
    role_update = role_update_schema.model_dump() if role_update_schema else {}
    return await access_control_service.update_role(role_id, role_update,*args,**kwargs)

async def delete_role(request:Request, role_id: str, *args:Any,**kwargs:Any):
    return await access_control_service.delete_role(role_id,*args,**kwargs)

async def get_many_roles(request:Request, roles_get_many_schema:RolesGetManySchema, *args:Any,**kwargs:Any) -> Tuple[List[Role],int]:
    get_many = roles_get_many_schema.model_dump() if roles_get_many_schema else {}
    return await access_control_service.get_many_roles(get_many, *args,**kwargs)


async def create_permission(request:Request, permission_create_schema:PermissionCreateSchema, *args: Any,**kwargs: Any) -> Permission:
    permission_create = permission_create_schema.model_dump() if permission_create_schema else {}
    return await access_control_service.create_permission(permission_create, *args,**kwargs)

async def get_permission(request:Request, permission_id: str, *args: Any,**kwargs: Any) -> Permission:
    return await access_control_service.get_permission(permission_id, *args,**kwargs)

async def update_permission(request:Request, permission_id: str, permission_update_data: PermissionUpdateSchema, *args: Any,**kwargs: Any) -> Permission:
    permission_update = permission_update_data.model_dump() if permission_update_data else {}
    return await access_control_service.update_permission(permission_id,permission_update, *args,**kwargs)

async def delete_permission(request:Request,permission_id: str, *args: Any,**kwargs: Any):
    return await access_control_service.delete_permission(permission_id, *args,**kwargs)

async def get_many_permissions(request:Request,permissions_get_many_schema: PermissionsGetManySchema, *args: Any,**kwargs: Any) -> Tuple[List[Permission],int]:
    get_many = permissions_get_many_schema.model_dump() if permissions_get_many_schema else {}
    return await access_control_service.get_many_permissions(get_many, *args,**kwargs)


async def create_user_role(request:Request,user_role_create_schema:UserRoleCreateSchema , *args: Any,**kwargs: Any) -> UserRole:
    user_role_create = user_role_create_schema.model_dump() if user_role_create_schema else {}
    return await access_control_service.create_user_role(user_role_create, *args,**kwargs)

async def get_user_roles(request:Request,user_id: str, *args: Any,**kwargs: Any) -> List[Role]:
    return await access_control_service.get_user_roles(user_id, *args,**kwargs)

async def delete_user_role(request:Request,user_id:str,role_id: str, *args: Any,**kwargs: Any):
    return await access_control_service.delete_user_role(user_id,role_id, *args,**kwargs)


async def create_role_permission(request:Request,role_permission_create_schema:RolePermissionCreateSchema , *args: Any,**kwargs: Any) -> RolePermission:
    role_permission_create = role_permission_create_schema.model_dump() if role_permission_create_schema else {}
    return await access_control_service.create_role_permission(role_permission_create, *args,**kwargs)

async def get_role_permissions(request:Request,role_id: str, *args: Any,**kwargs: Any) -> List[Permission]:
    return await access_control_service.get_role_permissions(role_id, *args,**kwargs)

async def delete_role_permission(request:Request,role_id: str,permission_id:str, *args: Any,**kwargs: Any):
    return await access_control_service.delete_role_permission(role_id,permission_id, *args,**kwargs)

async def has_permission(request:Request,user_id:str,action:str,resource:str, *args: Any,**kwargs: Any) -> bool:
    return await access_control_service.has_permission(user_id,action,resource, *args,**kwargs)





# async def create_roles_permissions_hierarchy(request: Request, roles_permissions_hierarchy_create_schema, *args: Any, **kwargs: Any):
#     roles_permissions_hierarchy_create = roles_permissions_hierarchy_create_schema if roles_permissions_hierarchy_create_schema else {}
#     return await access_control_service.create_roles_permissions_hierarchy(roles_permissions_hierarchy_create)

# async def get_roles_permissions_hierarchy(request: Request, role_id: str, *args: Any, **kwargs: Any):
#     return await access_control_service.get_roles_permissions_hierarchy(role_id)

# async def update_roles_permissions_hierarchy(request: Request, role_id: str, roles_permissions_hierarchy_update_schema, *args: Any, **kwargs: Any):
#     roles_permissions_hierarchy_update = roles_permissions_hierarchy_update_schema if roles_permissions_hierarchy_update_schema else {}
#     return await access_control_service.update_roles_permissions_hierarchy(role_id, roles_permissions_hierarchy_update)

# async def delete_roles_permissions_hierarchy(request: Request, role_id: str, *args: Any, **kwargs: Any):
#     return await access_control_service.delete_roles_permissions_hierarchy(role_id)


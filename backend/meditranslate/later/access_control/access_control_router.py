from fastapi import APIRouter,Request,Query
from meditranslate.src.access_control import access_control_controller
from meditranslate.app.shared.schemas import MetaSchema, PaginationSchema
from typing import Any,List,Annotated
from meditranslate.src.access_control.access_control_schemas import (
    RoleResponseSchema,
    RolesResponseSchema,
    RoleCreateSchema,
    RoleUpdateSchema,
    RolesGetManySchema,
    PermissionCreateSchema,
    PermissionUpdateSchema,
    PermissionsGetManySchema,
    RoleHierarchyCreateSchema,
    RoleHierarchyResponseSchema,
    PermissionResponseSchema,
    UserRoleCreateSchema,
    RolePermissionCreateSchema,
    PermissionsResponseSchema
)


access_control_router = APIRouter()

@access_control_router.post("/roles", response_model=RoleResponseSchema,status_code=201)
async def create_role(request: Request, role_create_schema: RoleCreateSchema) -> Any:
    role = await access_control_controller.create_role(request, role_create_schema,[], {})
    return RoleResponseSchema(
        data=role.as_dict(),
        status_code=201,
    )

@access_control_router.get("/roles/{role_id}", response_model=RoleResponseSchema, status_code=200)
async def get_role(request: Request, role_id: str) -> Any:
    role = await access_control_controller.get_role(request, role_id,[], {})
    return RoleResponseSchema(
        data=role.as_dict(),
        status_code=200,
    )

@access_control_router.put("/roles/{role_id}", response_model=RoleResponseSchema, status_code=200)
async def update_role(request: Request, role_id: str, role: RoleUpdateSchema) -> Any:
    role = await access_control_controller.update_role(request, role_id, role,[], {})
    return RoleResponseSchema(
        data=role.as_dict(),
        status_code=200,
    )

@access_control_router.delete("/roles/{role_id}", status_code=200)
async def delete_role(request: Request, role_id: str) -> Any:
    await access_control_controller.delete_role(request, role_id,[], {})

@access_control_router.get("/roles", response_model=RolesResponseSchema)
async def get_many_roles(
    request: Request,
    roles_get_many_schema:Annotated[RolesGetManySchema, Query()]=None
) -> Any:

    roles,total = await access_control_controller.get_many_roles(request, roles_get_many_schema,[], {})
    meta = None
    if roles_get_many_schema:
        schema = roles_get_many_schema.model_dump()
        if schema.get("limit",None) is not None and schema.get("offset",None) is not None:
            page_size = roles_get_many_schema.limit
            page = (roles_get_many_schema.offset // roles_get_many_schema.limit) + 1
            pagination = PaginationSchema(
                total=total,
                page=page,
                page_size=page_size
            )
            meta = MetaSchema(
                pagination=pagination
            )
    return RolesResponseSchema(
        data=[role.as_dict() for role in roles],
        status_code=200,
        meta=meta.model_dump()
    )

# Permission Endpoints
@access_control_router.post("/permissions", response_model=PermissionResponseSchema, status_code=201)
async def create_permission(request: Request, permission_create_schema: PermissionCreateSchema) -> Any:
    permission = await access_control_controller.create_permission(request, permission_create_schema,[], {})
    return PermissionResponseSchema(
        data=permission.as_dict(),
        status_code=200
    )

@access_control_router.get("/permissions/{permission_id}", response_model=PermissionResponseSchema, status_code=200)
async def get_permission(request: Request, permission_id: str) -> Any:
    permission = await access_control_controller.get_permission(request, permission_id,[], {})
    return PermissionResponseSchema(
        data=permission.as_dict(),
        status_code=200
    )

@access_control_router.put("/permissions/{permission_id}", response_model=PermissionResponseSchema, status_code=200)
async def update_permission(request: Request, permission_id: str, permission: PermissionUpdateSchema) -> Any:
    permission = await access_control_controller.update_permission(request, permission_id, permission,[], {})
    return PermissionResponseSchema(
        data=permission.as_dict(),
        status_code=200
    )

@access_control_router.delete("/permissions/{permission_id}", status_code=200)
async def delete_permission(request: Request, permission_id: str) -> Any:
    await access_control_controller.delete_permission(request, permission_id,[], {})

@access_control_router.get("/permissions", response_model=PermissionsResponseSchema,status_code=200)
async def get_many_permissions(
    request: Request,
    permissions_get_many_schema:Annotated[PermissionsGetManySchema, Query()]=None
):
    permissions,total = await access_control_controller.get_many_permissions(request, permissions_get_many_schema,[], {})
    meta = None
    if permissions_get_many_schema:
        schema = permissions_get_many_schema.model_dump()
        if schema.get("limit",None) is not None and schema.get("offset",None) is not None:
            page_size = permissions_get_many_schema.limit
            page = (permissions_get_many_schema.offset // permissions_get_many_schema.limit) + 1
            pagination = PaginationSchema(
                total=total,
                page=page,
                page_size=page_size
            )
            meta = MetaSchema(
                pagination=pagination
            )
    return PermissionsResponseSchema(
        data=[permission.as_dict() for permission in permissions],
        status_code=200,
        meta=meta.model_dump()
    )


@access_control_router.get("/role/{role_id}/permissions",response_model=PermissionsResponseSchema, status_code=200)
async def get_role_permissions(request: Request, role_id: str) -> Any:
    permissions = await access_control_controller.get_role_permissions(request, role_id,[], {})
    return PermissionsResponseSchema(
        data=[permission.as_dict() for permission in permissions],
        status_code=200
    )

@access_control_router.post("/role/{role_id}/permissions" , status_code=201)
async def create_role_permission(request: Request, role_permission_create_schema: RolePermissionCreateSchema) -> Any:
    await access_control_controller.create_role_permission(request, role_permission_create_schema,[], {})

@access_control_router.delete("/role/{role_id}/permissions/{permission_id}", status_code=200)
async def delete_role_permission(request: Request, role_id: str, permission_id:str) -> Any:
    await access_control_controller.delete_role_permission(request, role_id, permission_id,[], {})


@access_control_router.post("/role-hierarchy",status_code=201)
async def create_role_hierarchy(request: Request, role_hierarchy_create_schema: RoleHierarchyCreateSchema) -> Any:
    await access_control_controller.create_role_hierarchy(request, role_hierarchy_create_schema,[], {})
    # return RoleHierarchyResponseSchema(
    #     data=role_hierarchy.as_dict(),
    #     status_code=200,
    # )

@access_control_router.get("/roles/{role_id}/parents", response_model=RolesResponseSchema,status_code=200)
async def get_role_parent_roles(request: Request, role_id: str) -> Any:
    roles = await access_control_controller.get_role_parent_roles(request, role_id,[], {})
    return RolesResponseSchema(
        data=[role.as_dict() for role in roles],
        status_code=200,
        message="Created Role Successfuly!"
    )

@access_control_router.get("/roles/{role_id}/children", response_model=RolesResponseSchema,status_code=200)
async def get_role_child_roles(request: Request, role_id: str) -> Any:
    roles = await access_control_controller.get_role_child_roles(request, role_id,[], {})
    return RolesResponseSchema(
        data=[role.as_dict() for role in roles],
        status_code=200,
        message="Created Role Successfuly!"
    )

@access_control_router.delete("/role-hierarchy/{parent_role_id}/{child_role_id}", status_code=200)
async def delete_role_hierarchy(request: Request, parent_role_id: str, child_role_id: str) -> Any:
    await access_control_controller.delete_role_hierarchy(request, parent_role_id, child_role_id,[], {})

@access_control_router.post("/user-roles", status_code=201)
async def create_user_role(request: Request, user_role_create_schema: UserRoleCreateSchema) -> Any:
    await access_control_controller.create_user_role(request, user_role_create_schema,[], {})

@access_control_router.get("/user-roles/{user_id}", response_model=RolesResponseSchema, status_code=200)
async def get_user_roles(request: Request, user_id: str) -> Any:
    roles = await access_control_controller.get_user_roles(request, user_id,[], {})
    return RolesResponseSchema(
        data=[role.as_dict() for role in roles],
        status_code=200,
    )

@access_control_router.delete("/user-roles/{user_id}/{role_id}", status_code=200)
async def delete_user_role(request: Request, user_id: str, role_id: str) -> Any:
    await access_control_controller.delete_user_role(request, user_id, role_id,[], {})

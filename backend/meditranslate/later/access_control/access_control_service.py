from meditranslate.src.access_control.role_repository import RoleRepository
from meditranslate.src.access_control.permission_repository import PermissionRepository
from meditranslate.src.access_control.user_role_repository import UserRoleRepository
from meditranslate.src.access_control.role_permission_repository import RolePermissionRepository

from typing import Any,Optional,Dict,List,Union,Set
from meditranslate.app.db.models import (
    Permission,
    Role,
    RolePermission,
    UserRole
)

from meditranslate.app.errors import AppError,ErrorSeverity,HTTPStatus,ErrorType
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import select,and_,exists
from sqlalchemy.orm import aliased



async def create_role(role_create_data: Dict[str,Any]) -> Role:
    ac_repo = RoleRepository()
    new_role = await ac_repo.create_role(role_create_data)
    return new_role

async def get_role(role_id: str) -> Role:
    ac_repo = RoleRepository()
    user = await ac_repo.get_role(role_id)
    return user

async def delete_role(role_id: str):
    ac_repo = RoleRepository()
    is_deleted = await ac_repo.delete_role(role_id)
    return is_deleted

async def update_role(role_id: str, role_update_data: Dict[str,Any]) -> Role:
    ac_repo = RoleRepository()
    role = await ac_repo.update_role(role_id,role_update_data)
    return role

async def get_many_roles(roles_get_many_schema: Dict[str,Any]):
    ac_repo = RoleRepository()
    users = await ac_repo.get_many_roles(schema=roles_get_many_schema)
    return users

async def create_permission(permission_create_schema:Dict[str,Any]) -> Permission:
    ac_repo = PermissionRepository()
    new_permission = await ac_repo.create_permission(permission_create_schema)
    return new_permission

async def get_permission(permission_id: str) -> Permission:
    ac_repo = PermissionRepository()
    permission = await ac_repo.get_permission(permission_id)
    return permission

async def update_permission(permission_id: str, permission_update_data: Dict[str,Any]) -> Permission:
    ac_repo = PermissionRepository()
    permission = await ac_repo.update_permission(permission_id,permission_update_data)
    return permission

async def delete_permission(permission_id: str):
    ac_repo = PermissionRepository()
    is_deleted = await ac_repo.delete_permission(permission_id)
    return is_deleted

async def get_many_permissions(permissions_get_many_schema: Dict[str,Any]) -> List[Permission]:
    ac_repo = PermissionRepository()
    users = await ac_repo.get_many_permissions(schema=permissions_get_many_schema)
    return users


async def create_user_role(user_role_create_schema:Dict[str,Any] ) -> UserRole:
    ac_repo = UserRoleRepository()
    new_role = await ac_repo.create_user_role(user_role_create_schema)
    return new_role

async def get_user_roles(user_id: str) -> List[Role]:
    ac_repo = UserRoleRepository()
    user_roles = await ac_repo.get_user_roles(user_id)
    return user_roles

async def delete_user_role(user_id:str,role_id: str):
    ac_repo = UserRoleRepository()
    is_deleted = await ac_repo.delete_user_role(user_id=user_id,role_id=role_id)
    return is_deleted


async def create_role_permission(role_permission_create_schema:Dict[str,Any] ):
    ac_repo = RolePermissionRepository()
    new_role = await ac_repo.create_role_permission(role_permission_create_schema)
    return new_role

async def get_role_permissions(role_id: str) -> List[Permission]:
    ac_repo = RolePermissionRepository()
    permissions = await ac_repo.get_role_permissions(role_id)
    return permissions

async def delete_role_permission(role_id: str,permission_id:str):
    ac_repo = RolePermissionRepository()
    is_deleted = await ac_repo.delete_role_permission(role_id=role_id,permission_id=permission_id)
    return is_deleted


from typing import List,Optional,Dict,Any,Union
from meditranslate.app.db.models import RolePermission,Permission,Role
from meditranslate.app.db import BaseRepository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import select,and_

from meditranslate.app.errors import AppError,ErrorSeverity,HTTPStatus,ErrorType


class RolePermissionRepository(BaseRepository[RolePermission]):

    def __init__(self):
        super().__init__(RolePermission)

    async def create_role_permission(self,role_permission_data:Dict[str,Any]):
        role_permission = RolePermission(**role_permission_data)
        async with self.get_session() as session:
            try:
                await session.begin()
                session.add(role_permission)
                await session.flush()
                await session.commit()
                await session.refresh(role_permission)

            except SQLAlchemyError as e:
                await session.rollback()
                raise AppError(
                    error=e,
                    error_class=SQLAlchemyError,
                    title="get_user_role sql alchemy",
                    description="get_user_role sql alchemy",
                    context="user role repository",
                    error_type=ErrorType.DATABASE_ERROR,
                    http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                    kwargs={},
                    severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                    operable=False,
                    user_message=None,
                    headers={}
                ) from e
        return role_permission

    async def get_role_permission(self, role_id:str,permission_id:str) -> Optional[RolePermission]:
        async with self.get_session() as session:
            try:
                await session.begin()
                result = await session.execute(
                    select(RolePermission)
                    .join(Role, Role.id == RolePermission.role_id)
                    .join(Permission, Permission.id == RolePermission.permission_id)
                    .where(and_(Role.id == role_id, Permission.id == permission_id))
                )
                role_permission = result.scalars().one_or_none()
                if role_permission is not None:
                    return role_permission
                else:
                    raise AppError(
                        error=None,
                        error_class=SQLAlchemyError,
                        title="get_user_role sql alchemy",
                        description="get_user_role sql alchemy",
                        context="user role repository",
                        error_type=ErrorType.DATABASE_ERROR,
                        http_status=HTTPStatus.NOT_FOUND,
                        kwargs={},
                        severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                        operable=False,
                        user_message=None,
                        headers={}
                    )
            except SQLAlchemyError as e:
                raise AppError(
                    error=e,
                    error_class=SQLAlchemyError,
                    title="get_user_role sql alchemy",
                    description="get_user_role sql alchemy",
                    context="user role repository",
                    error_type=ErrorType.DATABASE_ERROR,
                    http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                    kwargs={},
                    severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                    operable=False,
                    user_message=None,
                    headers={}
                ) from e

    async def get_role_permissions(self, role_id:str) -> Optional[List[Permission]]:
        async with self.get_session() as session:
            try:
                await session.begin()
                result = await session.execute(
                    select(Permission)
                    .join(RolePermission, RolePermission.permission_id == Permission.id)
                    .join(Role, Role.id == RolePermission.role_id)
                    .where(Role.id == role_id)
                )
                permissions = result.scalars().all()
                return permissions if permissions else []
            except SQLAlchemyError as e:
                raise AppError(
                    error=e,
                    error_class=SQLAlchemyError,
                    title="get_user_role sql alchemy",
                    description="get_user_role sql alchemy",
                    context="user role repository",
                    error_type=ErrorType.DATABASE_ERROR,
                    http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                    kwargs={},
                    severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                    operable=False,
                    user_message=None,
                    headers={}
                ) from e

    async def delete_role_permission(self, role_id:str, permission_id: str) -> bool:
        async with self.get_session() as session:
            try:
                await session.begin()
                result = await session.execute(
                    select(RolePermission)
                    .join(Role, Role.id == RolePermission.role_id)
                    .join(Permission, Permission.id == RolePermission.permission_id)
                    .where(and_(Role.id == role_id, Permission.id == permission_id))
                )
                role_permission = result.scalars().one_or_none()
                if role_permission:
                    await session.delete(role_permission)
                    await session.commit()
                    return True
                else:
                    raise AppError(
                        error=None,
                        error_class=SQLAlchemyError,
                        title="get_user_role sql alchemy",
                        description="get_user_role sql alchemy",
                        context="user role repository",
                        error_type=ErrorType.DATABASE_ERROR,
                        http_status=HTTPStatus.NOT_FOUND,
                        kwargs={},
                        severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                        operable=False,
                        user_message=None,
                        headers={}
                    )
            except SQLAlchemyError as e:
                await session.rollback()
                raise AppError(
                    error=e,
                    error_class=SQLAlchemyError,
                    title="get_user_role sql alchemy",
                    description="get_user_role sql alchemy",
                    context="user role repository",
                    error_type=ErrorType.DATABASE_ERROR,
                    http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                    kwargs={},
                    severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                    operable=False,
                    user_message=None,
                    headers={}
                ) from e


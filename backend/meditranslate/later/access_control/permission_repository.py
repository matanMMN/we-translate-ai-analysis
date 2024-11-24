from typing import List,Optional,Dict,Any
from meditranslate.app.shared.schemas import GetManySchema, SortOrder
from meditranslate.app.db.models import Permission
from meditranslate.app.db import BaseRepository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import select,and_


from meditranslate.app.errors.app_error import AppError,ErrorSeverity,HTTPStatus,ErrorType


class PermissionRepository(BaseRepository[Permission]):

    def __init__(self):
        super().__init__(Permission)

    async def create_permission(self,permission_data:Dict[str,Any]):
        permission = Permission(**permission_data)
        async with self.get_session() as session:
            try:
                await session.begin()
                session.add(permission)
                await session.flush()
                await session.commit()
                await session.refresh(permission)

            except SQLAlchemyError as e:
                await session.rollback()
                raise AppError(
                    error=e,
                    error_class=SQLAlchemyError,
                    title="",
                    description="",
                    context="",
                    error_type=ErrorType.CLIENT_ERROR,
                    http_status=HTTPStatus.CONFLICT,
                    kwargs={},
                    severity=ErrorSeverity.CRITICAL_SHUTDOWN,
                    operable=True,
                    user_message=None,
                    headers={}
                ) from e
        return permission


    async def get_permission(self, permission_id: str) -> Optional[Permission]:
        async with self.get_session() as session:
            try:
                await session.begin()
                result = await session.execute(select(Permission).where(Permission.id == permission_id))
                permission = result.scalars().one_or_none()
                if permission is not None:
                    return permission
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


    async def update_permission(self, permission_id: str, permission_update_data: Dict[str, Any]) -> Optional[Permission]:
        async with self.get_session() as session:
            try:
                await session.begin()
                result = await session.execute(select(Permission).where(Permission.id == permission_id))
                permission = result.scalars().one_or_none()
                if permission is not None:
                    for key, value in permission_update_data.items():
                        if value:
                            setattr(permission, key, value)
                    await session.commit()
                    await session.refresh(permission)
                    return permission
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


    async def delete_permission(self, permission_id: str) -> bool:
        async with self.get_session() as session:
            try:
                await session.begin()
                result = await session.execute(select(Permission).where(Permission.id == permission_id))
                permission = result.scalars().one_or_none()
                if permission:
                    await session.delete(permission)
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


    async def get_many_permissions(self, schema:GetManySchema) -> List[Permission]:
        return await self.get_many(schema=schema)


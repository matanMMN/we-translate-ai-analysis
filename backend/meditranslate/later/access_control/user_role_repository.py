"""da c"""
from meditranslate.app.db import BaseRepository
from meditranslate.app.errors import AppError,ErrorSeverity,HTTPStatus,ErrorType

from meditranslate.app.db.models import UserRole,Role,User
from typing import List,Optional,Dict,Any
from sqlalchemy.sql import select,and_
from sqlalchemy.exc import SQLAlchemyError


class UserRoleRepository(BaseRepository[UserRole]):

    def __init__(self):
        super().__init__(UserRole)

    async def create_user_role(self,user_role_data:Dict[str,Any]):
        user_role = UserRole(**user_role_data)
        async with self.get_session() as session:
            try:
                await session.begin()
                session.add(user_role)
                await session.flush()
                await session.commit()
                await session.refresh(user_role)

            except SQLAlchemyError as e:
                await session.rollback()
                raise AppError(
                    error=e,
                    error_class=SQLAlchemyError,
                    title="create_user_role sql alchemy",
                    description="create_user_role sql alchemy",
                    context="user role repository",
                    error_type=ErrorType.DATABASE_ERROR,
                    http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                    kwargs={},
                    severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                    operable=False,
                    user_message=None,
                    headers={}
                ) from e
        return user_role

    async def get_user_role(self, user_id:str,role_id:str) -> Optional[UserRole]:
        async with self.get_session() as session:
            try:
                await session.begin()
                result = await session.execute(
                    select(UserRole)
                    .join(Role, Role.id == UserRole.role_id)  # Join with Role table
                    .join(User, User.id == UserRole.user_id)  # Join with User table
                    .where(and_(Role.id == role_id, User.id == user_id))
                )
                user_role = result.scalars().one_or_none()
                if user_role is not None:
                    return user_role
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

    async def get_user_roles(self, user_id:str) -> Optional[List[Role]]:
        async with self.get_session() as session:
            try:
                await session.begin()
                result = await session.execute(
                    select(Role)
                    .join(UserRole,UserRole.role_id == Role.id)
                    .where(UserRole.user_id == user_id)
                )
                roles = result.scalars().all()
                return roles if roles else None
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

    async def delete_user_role(self, user_id:str, role_id: str) -> bool:
        async with self.get_session() as session:
            try:
                await session.begin()
                result = await session.execute(
                    select(UserRole)
                    .join(Role, Role.id == UserRole.role_id)  # Join with Role table
                    .join(User, User.id == UserRole.user_id)  # Join with User table
                    .where(and_(Role.id == role_id, User.id == user_id))
                )
                user_role = result.scalars().one_or_none()
                if user_role is not None:
                    await session.delete(user_role)
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

    async def get_role_users(self, role_id:str) -> Optional[List[User]]:
        async with self.get_session() as session:
            try:
                await session.begin()
                result = await session.execute(
                    select(User)
                    .join(UserRole,UserRole.user_id == User.id)
                    .join(Role, Role.id == UserRole.role_id)
                    .where(Role.id == role_id)
                )
                users = result.scalars().all()
                return users if users else None
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

from typing import List,Optional,Dict,Any
from meditranslate.app.shared.schemas import GetManySchema
from meditranslate.app.db.models import Role
from meditranslate.app.db import BaseRepository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import select
from meditranslate.app.errors import AppError,ErrorSeverity,HTTPStatus,ErrorType

class RoleRepository(BaseRepository[Role]):

    def __init__(self):
        super().__init__(Role)

    async def create_role(self,role_data:Dict[str,Any]):
        role = Role(**role_data)
        async with self.get_session() as session:
            try:
                await session.begin()
                session.add(role)

                await session.flush()
                await session.commit()
                await session.refresh(role)

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
        return role


    async def get_role(self, role_id: str) -> Optional[Role]:
        async with self.get_session() as session:
            try:
                result = await session.execute(select(Role).where(Role.id == role_id))
                role = result.scalars().one_or_none()
                if role is not None:
                    return role
                else:
                    raise AppError(
                        error=None,
                        error_class=Exception,
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


    async def update_role(self, role_id: str, role_update_data: Dict[str, Any]) -> Optional[Role]:
        async with self.get_session() as session:
            try:
                result = await session.execute(select(Role).where(Role.id == role_id))
                role = result.scalars().one_or_none()
                if role is not None:
                    for key, value in role_update_data.items():
                        if value:
                            setattr(role, key, value)  # Update attributes
                    await session.commit()  # Commit the transaction
                    await session.refresh(role)  # Refresh the user
                    return role
                else:
                    raise AppError(
                        error=None,
                        error_class=Exception,
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


    async def delete_role(self, role_id: str) -> bool:
        async with self.get_session() as session:
            try:
                result = await session.execute(select(Role).where(Role.id == role_id))
                role = result.scalars().one_or_none()
                if role is not None:
                    await session.delete(role)
                    await session.commit()
                    return True
                else:
                    raise AppError(
                        error=None,
                        error_class=Exception,
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

    async def get_many_roles(self, schema:GetManySchema) -> List[Role]:
        return await self.get_many(schema=schema)


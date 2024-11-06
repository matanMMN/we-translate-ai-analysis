from typing import Any,Dict,List,Optional,Tuple

from meditranslate.app.db.transaction import Propagation, Transactional
from .user_repository import UserRepository
from meditranslate.app.db.models import User
from meditranslate.app.shared.base_service import BaseService
from meditranslate.utils.security.password import hash_password
from meditranslate.app.errors import AppError,ErrorSeverity,ErrorType,HTTPStatus
from meditranslate.src.users.user_schemas import (
    UserCreateSchema,
    GetManySchema,
    UserUpdateSchema
)

class UserService(BaseService[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    def _to_public(self,user:User) -> dict:
        public_user = user.as_dict()
        public_user.pop("hashed_password")
        return public_user


    async def get_user_by_username(self,username:str) -> Optional[User]:
        user = await self.user_repository.get_by(field="username",value=username,joins=None,unique=True)
        return user

    async def create_user(self,user_create_schema: UserCreateSchema) -> User:

        new_user_data = user_create_schema.model_dump()
        new_user_data.pop("id",None)
        password = new_user_data.pop("password",None)
        new_user_data['hashed_password'] = hash_password(password)
        new_user = await self.user_repository.create(new_user_data)
        public_user = self._to_public(new_user)
        return public_user

    async def get_user(self,user_id: str) -> User:
        user = await self.user_repository.get_by(field="id",value=user_id,joins=None,unique=True)
        if not user:
            raise AppError(
                title="get user endpoint",
                http_status=HTTPStatus.NOT_FOUND,
                user_message="User was not found",
            )
        public_user = self._to_public(user)
        return public_user

    async def update_user(self,user_id: str, user_update_data: UserUpdateSchema) -> None:
        update_user_data = user_update_data.model_dump()
        password = update_user_data.pop("password",None)
        update_user_data.pop("id",None)
        if password is not None:
            update_user_data['hashed_password'] = hash_password(password)
        user = await self.user_repository.get_by("id",user_id,unique=True)
        if not user:
            raise AppError(
                title="update user endpoint",
                http_status=HTTPStatus.NOT_FOUND,
            )
        return await self.user_repository.update(user,update_user_data)

    async def delete_user(self,user_id: str) -> None:
        user = await self.user_repository.get_by("id",user_id,unique=True)
        if not user:
            raise AppError(
                title="delete user endpoint",
                http_status=HTTPStatus.NOT_FOUND
            )
        return await self.user_repository.delete(user)

    async def get_many_users(self,users_get_many_schema: GetManySchema) -> Tuple[List[User],int]:
        users,total = await self.user_repository.get_many(**users_get_many_schema.model_dump())
        public_users = []
        for user in users:
            public_users.append(self._to_public(user))
        return public_users,total

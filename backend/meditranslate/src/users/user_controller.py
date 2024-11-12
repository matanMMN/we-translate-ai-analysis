from typing import Any, List,Optional
from meditranslate.app.shared.base_controller import BaseController
from meditranslate.src.users.user_service import UserService
from meditranslate.src.users.user_schemas import (
    UserCreateSchema,
    GetManySchema,
    UserUpdateSchema
)
from meditranslate.app.db.models import User
from meditranslate.app.db.transaction import Transactional,Propagation


class UserController(BaseController[User]):
    def __init__(self, user_service:UserService) -> None:
        super().__init__(User,user_service)
        self.user_service:UserService = user_service

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def create_user(self,current_user:User,user_create_schema:UserCreateSchema) -> User:
        return await self.user_service.create_user(current_user,user_create_schema)

    async def get_user(self,user_id: str,raise_exception:bool=True,is_public:bool=True) -> Optional[User]:
        return await self.user_service.get_user(user_id,raise_exception,is_public)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_user(self,current_user:User,user_id: str, user_update_schema:UserUpdateSchema) -> None:
        return await self.user_service.update_user(current_user,user_id, user_update_schema)

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def delete_user(self,current_user:User,user_id: str) -> None:
        return await self.user_service.delete_user(current_user,user_id)

    async def get_many_users(self,users_get_many_schema:GetManySchema) -> List[User]:
        return await self.user_service.get_many_users(users_get_many_schema)

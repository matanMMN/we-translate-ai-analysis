from typing import Any, List

from fastapi import Request

from meditranslate.app.db.transaction import Propagation, Transactional
from meditranslate.app.shared.base_controller import BaseController
from meditranslate.src.users.user import User
from meditranslate.src.auth.auth_service import AuthService
from .auth_schemas import (
    LoginSchema,
    RegisterUserSchema
)



class AuthController(BaseController[User]):
    def __init__(self, auth_service:AuthService):
        super().__init__(User, auth_service)
        self.auth_service = auth_service

    async def login(self,login_schema:LoginSchema):
        return await self.auth_service.login(login_schema)

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def register_user(self,register_user_schema:RegisterUserSchema):
        return await self.auth_service.register_user(register_user_schema)


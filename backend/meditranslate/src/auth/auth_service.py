"""Module providing a function printing python version."""

from typing import Any,Dict,List

from pydantic import BaseModel
from meditranslate.app.shared.base_service import BaseService
from meditranslate.src.auth.auth_schemas import LoginSchema
from meditranslate.src.users.user import User
from meditranslate.src.users.user_repository import UserRepository

import asyncio
from meditranslate.app.errors import AppError,ErrorSeverity,HTTPStatus,ErrorType
from meditranslate.utils.security.json_web_tokens import create_jwt_token
from meditranslate.utils.security.password import verify_password
from meditranslate.app.configurations import config
from meditranslate.src.auth.auth_constants import JWTData



class AuthService(BaseService[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    async def login(self,login_schema: LoginSchema):
        username = login_schema.username
        password = login_schema.password
        user = await self.user_repository.get_by("username",username,unique=True)
        if not user:
            raise AppError(
                error_type=ErrorType.AUTHENTICATION_ERROR,
                http_status=HTTPStatus.NOT_FOUND,
                user_message="wrong username"
            )
        else:
            is_valid = verify_password(password,user.hashed_password)
            if not is_valid or is_valid is False:
                raise AppError(
                    error_type=ErrorType.AUTHENTICATION_ERROR,
                    http_status=HTTPStatus.NOT_FOUND,
                    user_message="wrong password"
                )
            else:
                data:JWTData = JWTData(
                    user_id=user.id,
                    username=user.username
                )
                token = create_jwt_token(
                    config.SECRET_KEY,
                    data=data.model_dump(),
                    expire_minutes=config.JWT_EXPIRE_MINUTES,
                    token_type="access_token",
                    algorithm=config.JWT_ALGORITHM
                )
                return token

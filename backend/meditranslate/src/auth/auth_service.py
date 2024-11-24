"""Module providing a function printing python version."""

from typing import Any,Dict,List

from pydantic import BaseModel
from meditranslate.app.shared.base_service import BaseService
from meditranslate.src.auth.auth_schemas import LoginSchema,RegisterUserSchema
from meditranslate.src.users.user import User
from meditranslate.src.users.user_repository import UserRepository

import asyncio
from meditranslate.app.errors import AppError,ErrorSeverity,HTTPStatus,ErrorType
from meditranslate.utils.security.json_web_tokens import create_jwt_token
from meditranslate.utils.security.password import hash_password, verify_password
from meditranslate.app.configurations import config
from meditranslate.src.auth.auth_constants import JWTData
from meditranslate.app.loggers import logger



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
                    http_status=HTTPStatus.UNAUTHORIZED,
                    user_message="Incorrect password"
                )
            else:
                data = JWTData(
                    user_id=user.id,
                    username=user.username
                )
                data = data.model_dump()
                token_type = "bearer"

                logger.debug(
                    f"""
                        encoding jwt:
                        {config.SECRET_KEY}
                        {str(data)}
                        {config.JWT_EXPIRE_MINUTES}
                        {token_type}
                        {config.JWT_ALGORITHM}
                    """
                )

                token = create_jwt_token(
                    config.SECRET_KEY,
                    data=data,
                    expire_minutes=config.JWT_EXPIRE_MINUTES,
                    token_type=token_type,
                    algorithm=config.JWT_ALGORITHM
                )
                return token

    async def register_user(self,register_user_schema:RegisterUserSchema) -> dict:
        new_user_data = register_user_schema.model_dump()
        password = new_user_data.pop("password",None)
        new_user_data['hashed_password'] = hash_password(password)
        new_user = await self.user_repository.create(new_user_data)
        public_user = new_user.as_dict()
        public_user.pop("hashed_password",None)
        public_user.pop("password",None)
        return public_user


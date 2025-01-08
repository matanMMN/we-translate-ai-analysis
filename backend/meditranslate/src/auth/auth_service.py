"""Module providing a function printing python version."""

from typing import Any,Dict,List
from meditranslate.utils.user_role.user_role import UserRole

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
        await self._validate_registration_data(new_user_data)
        password = new_user_data.pop("password", None)
        if not password:
            logger.error("Password is required")
            raise AppError(
                error_type=ErrorType.VALIDATION_ERROR,
                http_status=HTTPStatus.BAD_REQUEST,
                user_message="Password is required"
            )
        new_user_data['hashed_password'] = hash_password(password)
        new_user_data.pop("password",None)
        try:
            new_user = await self.user_repository.create(new_user_data)
            public_user = new_user.as_dict()
            public_user.pop("hashed_password",None)
            return public_user
        except Exception as e:
            logger.error(f"Failed to create user: {str(e)}")
            raise AppError(
                error_type=ErrorType.DATABASE_ERROR,
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                user_message="Failed to create user"
            )

    async def _validate_registration_data(self, data: Dict[str, Any]) -> None:
            """Validate registration data before user creation"""
            logger.debug("Validating registration data")

            # Validate role
            role = data.get("role")
            if role is not None:
                try:
                    UserRole(role)  # This will raise ValueError if role is invalid
                except ValueError:
                    logger.error(f"Invalid role provided: {role}")
                    valid_roles = [r.value for r in UserRole]
                    raise AppError(
                        error_type=ErrorType.VALIDATION_ERROR,
                        http_status=HTTPStatus.BAD_REQUEST,
                        user_message=f"Invalid role. Must be one of: {', '.join(valid_roles)}"
                    )

            # Check if username already exists
            existing_user = await self.user_repository.get_by(
                field="username",
                value=data["username"],
                unique=True
            )
            if existing_user:
                logger.error(f"Username already exists: {data['username']}")
                raise AppError(
                    error_type=ErrorType.VALIDATION_ERROR,
                    http_status=HTTPStatus.CONFLICT,
                    user_message="Username already exists"
                )

            # Check if email already exists
            if "email" in data and data["email"]:
                existing_email = await self.user_repository.get_by(
                    field="email",
                    value=data["email"],
                    unique=True
                )
                if existing_email:
                    logger.error(f"Email already exists: {data['email']}")
                    raise AppError(
                        error_type=ErrorType.VALIDATION_ERROR,
                        http_status=HTTPStatus.CONFLICT,
                        user_message="Email already exists"
                    )

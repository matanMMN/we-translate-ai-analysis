from typing import Annotated
from fastapi import Depends
from meditranslate.src.users.user_controller import UserController
from meditranslate.utils.security.json_web_tokens import decode_jwt_token,JWTPayload,JWTDecodeError,JWTExpiredError
from meditranslate.app.configurations import config
from fastapi import status
from pydantic import ValidationError
from fastapi import HTTPException
from meditranslate.app.db.models import User
from meditranslate.app.dependancies.auth import TokenDep
from meditranslate.app.shared.factory import Factory
from fastapi import Depends
from meditranslate.src.auth.auth_constants import JWTData
from meditranslate.app.loggers import logger


async def get_current_user(user_controller: Annotated[UserController,Depends(Factory.get_user_controller)], token: TokenDep) -> User:
    try:
        payload = decode_jwt_token(secret_key=config.SECRET_KEY,token=token,algorithms=[config.JWT_ALGORITHM])
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation Error {str(e)}",
        )
    except JWTDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failed to decode {str(e)}",
        )
    except JWTExpiredError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"expired token {str(e)}",
        )
    try:
        token_data = JWTPayload(**payload)
        data:JWTData = token_data.data
        user_id = data.user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"JWTPayload Payload Extraction Error {str(e)}",
        )
    user = user_controller.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    # for real time can check if hes already log in here in session
    # or checking if user is disabled
    return current_user


CurrentUserDep = Annotated[User, Depends(get_current_active_user)]

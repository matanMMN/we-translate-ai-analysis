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
import json

async def get_current_user(user_controller: Annotated[UserController,Depends(Factory.get_user_controller)], token: TokenDep) -> User:
    try:
        logger.debug(
            f"""
                decoding jwt token:
                {config.SECRET_KEY}
                {token}
                {config.JWT_ALGORITHM}
            """
        )
        payload = decode_jwt_token(secret_key=config.SECRET_KEY,token=token,algorithms=[config.JWT_ALGORITHM])
    except ValidationError as e:
        logger.error(f"exception in validation in jwt  data after successful decoding {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unauth",
        )
    except JWTDecodeError as e:
        logger.error(f"exception in deconding in jwt  data after successful decoding {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unauth",
        )
    except JWTExpiredError as e:
        logger.error(f"exception in expired in jwt  data after successful decoding {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="unauth"
        )
    try:
        token_data:JWTPayload = JWTPayload(**payload)
        data = JWTData(**token_data.data)
        logger.error(data)
        user_id = data.user_id
        logger.error("user_id")
        logger.error(user_id)
    except Exception as e:
        logger.error(f"exception in parsing jwt data after successful decoding {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"unauth",
        )
    logger.error(user_id)
    user = await user_controller.get_user(user_id,raise_exception=False,is_public=False)
    if user is None:
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

from fastapi import Depends
from fastapi.security import  OAuth2PasswordBearer
from meditranslate.app.errors import AppError
import http
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
TokenDep = Annotated[str, Depends(oauth2_scheme)]

class AuthenticationRequired:
    def __init__(
        self,
        token: TokenDep,
    ):
        if not token:
            raise AppError(
                title="AuthenticationRequired required",
                description="Authentication required",
                http_status=http.HTTPStatus.UNAUTHORIZED,
                user_message="No Bearer Token In Header"
            )




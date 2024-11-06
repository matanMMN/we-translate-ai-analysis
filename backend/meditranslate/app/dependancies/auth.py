from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from meditranslate.app.errors import AppError
import http
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthenticationRequired:
    def __init__(
        self,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    ):
        if not token:
            raise AppError(
                title="AuthenticationRequired required",
                description="Authentication required",
                http_status=http.HTTPStatus.UNAUTHORIZED,
                user_message="Invalid Access Token"
            )



TokenDep = Annotated[str, Depends(AuthenticationRequired)]
Annotated[str, Depends(oauth2_scheme)]

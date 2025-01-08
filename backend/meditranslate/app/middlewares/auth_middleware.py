from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from meditranslate.app.auth.permissions import ROLE_PERMISSIONS
from meditranslate.app.loggers import logger

class AuthorizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth check for authentication endpoints
        if request.url.path in ["/auth/login", "/auth/register"]:
            return await call_next(request)

        # Get current user from request state (set by authentication middleware)
        current_user = getattr(request.state, "user", None)
        
        if current_user:
            # Add user permissions to request state for use in endpoints
            request.state.permissions = ROLE_PERMISSIONS.get(current_user.role, [])
            logger.debug(
                f"User {current_user.id} with role {current_user.role} "
                f"has permissions: {request.state.permissions}"
            )
        
        return await call_next(request) 
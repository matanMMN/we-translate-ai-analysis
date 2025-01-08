from enum import Enum
from typing import List
from functools import wraps
from fastapi import HTTPException, status
from meditranslate.src.users.user import UserRole
from meditranslate.app.loggers import logger

class Permission(str, Enum):
    # Project permissions
    PROJECT_CREATE = "project:create"
    PROJECT_DELETE = "project:delete"  # Direct project deletion
    PROJECT_UPDATE = "project:update"
    PROJECT_DELETE_REQUEST = "project:delete:request"  # Request for project deletion
    
    # File permissions
    FILE_UPLOAD = "file:upload"
    
    # Term permissions
    TERM_REQUEST = "term:request"
    TERM_MANAGE = "term:manage"  # For approving/rejecting term requests
    
    # Request permissions
    REQUEST_MANAGE = "request:manage"  # For handling any type of requests

# Define role-based permissions
ROLE_PERMISSIONS = {
    UserRole.GENERAL_MANAGER: [
        permission.value for permission in Permission  # Has access to all permissions
    ],
    UserRole.PROJECT_MANAGER: [
        Permission.PROJECT_CREATE,
        Permission.PROJECT_DELETE,
        Permission.PROJECT_UPDATE,
        Permission.REQUEST_MANAGE,
        Permission.TERM_MANAGE,
        Permission.FILE_UPLOAD
    ],
    UserRole.TRANSLATOR: [
        Permission.PROJECT_CREATE,
        Permission.PROJECT_DELETE_REQUEST,  
        Permission.FILE_UPLOAD,
        Permission.TERM_REQUEST
    ],
    UserRole.LANGUAGE_REVIEWER: [
        Permission.PROJECT_CREATE,
        Permission.PROJECT_DELETE_REQUEST, 
        Permission.FILE_UPLOAD,
        Permission.TERM_REQUEST
    ],
    UserRole.QA_MANAGER: [
        Permission.PROJECT_CREATE,
        Permission.PROJECT_DELETE_REQUEST, 
        Permission.FILE_UPLOAD,
        Permission.TERM_REQUEST
    ]
}

def requires_permissions(required_permissions: List[Permission]):
    """
    Decorator to check if user has required permissions based on their role
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from kwargs
            current_user = kwargs.get('current_user')
            if not current_user:
                logger.error("No user found in request")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

            # Get permissions for user's role
            user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])

            # Check if user has all required permissions
            missing_permissions = [
                perm for perm in required_permissions 
                if perm.value not in user_permissions
            ]

            if missing_permissions:
                logger.warning(
                    f"User {current_user.id} with role {current_user.role} "
                    f"attempted to access endpoint requiring permissions: {missing_permissions}"
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )

            return await func(*args, **kwargs)
        return wrapper
    return decorator
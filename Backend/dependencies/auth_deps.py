from fastapi import Depends, HTTPException, status
from ..middleware.auth_middleware import AuthMiddleware
from ..models.user import User

auth_handler = AuthMiddleware()

async def get_current_user(user: User = Depends(auth_handler)) -> User:
    """Dependency to get current authenticated user"""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user 
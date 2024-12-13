from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..utils.jwt_utils import verify_token
from ..models.user import User
from typing import Optional

security = HTTPBearer()

class AuthMiddleware:
    async def __call__(self, request: Request) -> Optional[User]:
        credentials: HTTPAuthorizationCredentials = await security(request)
        
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code"
            )
        
        token = credentials.credentials
        payload = verify_token(token)
        
        user = await User.find_one({"_id": payload.get("user_id")})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user

# Usage in routes:
auth_handler = AuthMiddleware() 
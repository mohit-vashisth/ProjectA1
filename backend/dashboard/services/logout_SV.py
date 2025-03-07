from fastapi import APIRouter, HTTPException, Request, Response, status
from backend.core import config
from backend.schemas.blacklist_token_schema import BlacklistToken
from backend.security.jwt_handler import check_blacklisted_token
from backend.utils.logger import init_logger

logout_route = APIRouter()
@logout_route.post(path=config.VITE_LOGOUT_EP, status_code=status.HTTP_200_OK)
async def logout(request: Request , response: Response):
    init_logger(message=f"logout attempt : method :{request.method} | url:{request.url} | cookies: {request.cookies}")
    
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "No access token found in cookies."
        )
    
    existing_token = await check_blacklisted_token(access_token)
    if existing_token:
        init_logger(message="Token is already blacklisted.")
        return {"message" : "Token is already blacklisted."}

    blacklist_token = BlacklistToken(token=access_token)

    await blacklist_token.insert()

    response.delete_cookie("access_token")
    init_logger(message="Access token has been blacklisted.")
    return {"message": "logged out successfully."}
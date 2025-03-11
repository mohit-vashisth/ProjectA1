from fastapi import APIRouter, HTTPException, Request, Response, status
from backend.core import config
from backend.schemas.token_scema import TokenType, Tokens
from backend.security.jwt_handler import check_blacklisted_token, verify_n_refresh_token
from backend.security.token_manager import get_cookies_token
from backend.utils.logger import init_logger

logout_route = APIRouter()
@logout_route.post(path=config.VITE_LOGOUT_EP, status_code=status.HTTP_200_OK)
async def logout(request: Request , response: Response):
    init_logger(message=f"logout attempt : method :{request.method} | url:{request.url} | cookies: {request.cookies}")
    
    access_token = get_cookies_token(request=request)
    await verify_n_refresh_token(request=request)
    if not access_token:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "No access token found in cookies."
        )
    email_id = "  "
    # if not email_id:
    #     raise HTTPException(
    #         status_code = status.HTTP_400_BAD_REQUEST,
    #         detail = "No email found in cookies."
    #     )
    
    existing_token = await check_blacklisted_token(access_token)
    if existing_token:
        init_logger(message="Token is already blacklisted.")
        return {"message" : "Token is already blacklisted."}

    blacklist_token = Tokens(
        email_ID=email_id,
        token=access_token,
        token_type=TokenType.BLACKLIST
        )

    await blacklist_token.insert()

    response.delete_cookie("access_token")
    init_logger(message="Access token has been blacklisted.")
    return {"message": "logged out successfully."}
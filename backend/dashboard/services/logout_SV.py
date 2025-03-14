import ast
import json
from fastapi import APIRouter, HTTPException, Request, Response, status
from authlib.jose import JWTClaims
from backend.core import config
from backend.schemas.token_scema import TokenType, Tokens
from backend.security.jwt_data_extract import get_jwt_email
from backend.security.token_verification import check_blacklisted_token, verify_n_refresh_token
from backend.security.get_cookies_tokens import get_cookies_access_token, get_cookies_refresh_token
from backend.utils.logger import init_logger

logout_route = APIRouter()

@logout_route.post(path=config.VITE_LOGOUT_EP, status_code=status.HTTP_200_OK)
async def logout(request: Request , response: Response):
    init_logger(message=f"logout attempt : method :{request.method} | url:{request.url} | cookies: {request.cookies}")
    
    access_token = get_cookies_access_token(request=request)
    refresh_token = get_cookies_refresh_token(request=request)
    payload = await verify_n_refresh_token(request=request)

    email_id = get_jwt_email(decoded_token=payload)
    
    await check_blacklisted_token(token=access_token)
    await check_blacklisted_token(token=refresh_token)

    blacklist_access_token = Tokens(
        email_ID=email_id,
        token=access_token,
        token_type=TokenType.BLACKLIST
        )

    await blacklist_access_token.insert()
    
    blacklist_refresh_token = Tokens(
        email_ID=email_id,
        token=refresh_token,
        token_type=TokenType.BLACKLIST
        )

    await blacklist_refresh_token.insert()

    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    init_logger(message="Access token has been blacklisted.")
    init_logger(message="Refresh token has been blacklisted.")
    init_logger(message="User logged out successfully.")
    return {"message": "logged out successfully."}
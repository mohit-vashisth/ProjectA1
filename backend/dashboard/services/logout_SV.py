import ast
import json
from fastapi import APIRouter, HTTPException, Request, Response, status
from authlib.jose import JWTClaims
from backend.core import config
from backend.schemas.token_schema import TokenType, Tokens
from backend.security.jwt_data_extract import get_jwt_email
from backend.security.token_verification import is_blacklisted_token, verify_and_refresh_token
from backend.security.get_cookies_tokens import get_cookies_access_token, get_cookies_refresh_token
from backend.utils.logger import init_logger

logout_route = APIRouter()

@logout_route.post(path=config.VITE_LOGOUT_EP, status_code=status.HTTP_200_OK)
async def logout(request: Request , response: Response):
    init_logger(message=f"logout attempt : method :{request.method} | url:{request.url} | cookies: {request.cookies}")
    
    access_token = get_cookies_access_token(request=request)
    init_logger(f"access token found:{access_token}", level="critical")
    refresh_token = get_cookies_refresh_token(request=request)
    init_logger(f"refresh token found:{refresh_token}", level="critical")
    payload = await verify_and_refresh_token(request=request)

    email_id = get_jwt_email(decoded_token=payload)
    
    await is_blacklisted_token(token=access_token)
    await is_blacklisted_token(token=refresh_token)

    blacklist_access_token = Tokens(
        email_ID=email_id,
        token=access_token,
        token_type=TokenType.BLACKLIST
        )

    
    blacklist_refresh_token = Tokens(
        email_ID=email_id,
        token=refresh_token,
        token_type=TokenType.BLACKLIST
        )
    
    await Tokens.find_one(
        Tokens.token == refresh_token,
        Tokens.token_type == TokenType.REFRESH
    ).delete()

    await blacklist_access_token.insert()
    await blacklist_refresh_token.insert()

    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    init_logger(message="Access token has been blacklisted.")
    init_logger(message="Refresh token has been blacklisted.")
    init_logger(message="User logged out successfully.")
    return {"message": "logged out successfully."}
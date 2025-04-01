from backend.core import config
from backend.utils.logger import init_logger
from backend.schemas.token_schema import TokenType, Tokens
from backend.security.jwt_data_extract import get_jwt_email
from backend.security.token_verification import is_blacklisted_token, verify_and_refresh_token
from backend.security.get_cookies_tokens import get_cookies_access_token, get_cookies_refresh_token

from fastapi import APIRouter, Request, Response, status

logout_route = APIRouter()

@logout_route.post(path=config.LOGOUT_EP, status_code=status.HTTP_200_OK)
async def logout(request: Request, response: Response):
    init_logger(message=f"Logout attempt: method={request.method} | url={request.url} | cookies={request.cookies}", request=request)

    access_token = get_cookies_access_token(request)
    refresh_token = get_cookies_refresh_token(request)

    init_logger(f"Access token found: {access_token}", request=request)
    init_logger(f"Refresh token found: {refresh_token}", request=request)

    payload = await verify_and_refresh_token(request)
    email_id = get_jwt_email(decoded_token=payload)

    await is_blacklisted_token(access_token)
    await is_blacklisted_token(refresh_token)

    blacklist_tokens = [
        Tokens(email_ID=email_id, token=access_token, token_type=TokenType.BLACKLIST),
        Tokens(email_ID=email_id, token=refresh_token, token_type=TokenType.BLACKLIST),
    ]

    await Tokens.find_one(
        Tokens.token == refresh_token,
        Tokens.token_type == TokenType.REFRESH
    ).delete()

    for token in blacklist_tokens:
        await token.insert()

    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    init_logger("Access and refresh tokens have been blacklisted.", request=request)
    init_logger("User logged out successfully.", request=request)

    return {"message": "Logged out successfully."}
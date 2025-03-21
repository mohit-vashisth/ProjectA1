from backend.core import config
from backend.utils.logger import init_logger
from backend.utils.load_keys import load_keys
from backend.schemas.token_schema import Tokens, TokenType
from backend.security.jwt_data_extract import get_jwt_email
from backend.security.create_jwt import create_refresh_token
from backend.security.get_cookies_tokens import get_cookies_access_token, get_cookies_refresh_token

from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from authlib.jose import jwt, JoseError

_, PUBLIC_KEY = load_keys()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.VITE_LOGIN_EP)

async def is_blacklisted_token(token: str) -> bool:
    init_logger(message=f"Checking if token is blacklisted: {token}")
    blacklisted = await Tokens.find_one({"token_type": TokenType.BLACKLIST, "token": token})
    return blacklisted is not None

async def verify_and_refresh_token(request: Request) -> str:
    try:
        access_token = get_cookies_access_token(request=request)
        init_logger(message=f"JWT Access Token Received: {access_token}")

        if not isinstance(access_token, str):
            init_logger(message="Invalid access token format received", level="warning")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token format"
            )

        payload = jwt.decode(access_token,PUBLIC_KEY, claims_options={
                "exp": {"essential": True},
                "email_ID": {"essential": True},
                "type": {"essential": True}
            }
        )
        
        init_logger(message="Verifying access token")

        payload.validate()

        if payload["type"] != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token type"
            )

        init_logger(message="Access token verified")
        return payload

    except JoseError as e:
        init_logger(message=f"Access token verification failed: {str(e)}", level="error")

        refresh_token = get_cookies_refresh_token(request=request)

        if not isinstance(refresh_token, str):
            init_logger(message="Missing or invalid refresh token. Please login again.", level="warning")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid refresh token found. Please login again."
            )

        if await is_blacklisted_token(token=refresh_token):
            init_logger(message="Refresh token is blacklisted", level="warning")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been blacklisted. Please log in again."
            )

        try:
            init_logger(message="Verifying refresh token")
            refresh_payload = jwt.decode(refresh_token, PUBLIC_KEY, claims_options={
                    "exp": {"essential": True},
                    "email_ID": {"essential": True},
                    "type": {"essential": True}
                }
            )
            
            refresh_payload.validate()

            if refresh_payload["type"] != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token type"
                )

            email_id = get_jwt_email(decoded_token=refresh_payload)
            user_info = {"email_ID": email_id}
            new_token = await create_refresh_token(user=user_info)

            init_logger(message="New token generated via refresh token")
            return new_token

        except JoseError as je:
            init_logger(message=f"Refresh token verification failed: {str(je)}", level="warning")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
        except Exception as exc:
            init_logger(message=f"Error while processing refresh token: {str(exc)}", level="error")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Error in refresh token processing"
            )

    except Exception as e:
        init_logger(message=f"Unexpected error in token verification: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while verifying token"
        )

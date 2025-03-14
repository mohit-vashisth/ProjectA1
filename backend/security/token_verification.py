from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from backend.core import config
from backend.schemas.token_scema import Tokens
from backend.security.get_cookies_tokens import get_cookies_access_token
from backend.security.create_jwt import create_access_token
from backend.utils.load_keys import load_keys
from backend.utils.logger import init_logger
from authlib.jose import jwt, JoseError

_, PUBLIC_KEY = load_keys()

async def validate_refresh_token(refresh_token: str | None):
    if refresh_token:
        await check_blacklisted_token(token="refresh_token")

        payload = jwt.decode(refresh_token, PUBLIC_KEY, claims_options={
            "exp": {"essential": True},
            "email_ID": {"essential": True},
            "type": {"essential": True}
        })

        init_logger(message="Verifying Refresh token")

        payload.validate()

        if payload["type"] != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
        init_logger(message="Verified Refresh token")

        return refresh_token
    
    init_logger(message="Invalid token format received", level="warning")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
          detail="Invalid token format"
    )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.VITE_LOGIN_EP)

async def verify_n_refresh_token(request: Request) -> str:
    try:
        access_token = get_cookies_access_token(request=request)
        
        init_logger(message=f"Jwt Token Received: {access_token}")
        if not isinstance(access_token, str):
            init_logger(message="Invalid token format received", level="warning")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                  detail="Invalid token format"
            )
        
        payload = jwt.decode(access_token, PUBLIC_KEY, claims_options={
            "exp": {"essential": True},
            "email_ID": {"essential": True},
            "type": {"essential": True}
        })

        init_logger(message="Verifying jwt token")

        payload.validate()
        await check_blacklisted_token(token=access_token)

        if payload["type"] != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

        init_logger(message="Verified jwt token")

        return payload 
    
    except JoseError as je:
        init_logger(message=f"JoseError in verify_access_token: {str(je)}", level="error")

        if "exp" in str(je):
            init_logger(message="Token expired, generating new token")

            try:
                expired_payload = jwt.decode(access_token, PUBLIC_KEY, validate=False)
                user_info = {
                    "email_ID": expired_payload["email_ID"],
                }

                new_token = await create_access_token(user=user_info)
                return new_token

            except Exception as e:
                init_logger(message=f"Error while extracting user info: {str(e)}", level="error")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Expired token is invalid"
                )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims"
        )
    
    except Exception as e:
        init_logger(message=f"Unexpected error in verify_access_token: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while verifying token"
        )
    
async def check_blacklisted_token(token:str) -> None: #isTokenExpBlk
    init_logger(message="Checking if token is blacklisted or not.")
    blacklisted = await Tokens.find_one({"token":token})
    if blacklisted:
        init_logger(message="The token is already blacklisted.")
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Token has been blacklisted. Please login again"
        )
    init_logger(message="The token is not Blacklisted.")
    return None

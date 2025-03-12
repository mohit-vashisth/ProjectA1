from backend.core import config
from backend.schemas.token_scema import TokenType, Tokens
from backend.security.token_manager import get_cookies_token
from backend.utils.logger import init_logger
from backend.utils.current_time import current_time

from authlib.jose import jwt, JoseError
from fastapi import HTTPException, Request, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer

try:
    init_logger(message="Loading Keys from Environment Variables")
    PRIVATE_KEY, PUBLIC_KEY = config.read_pv_key()
    init_logger(message="Key Loaded successfully...")

    if not PRIVATE_KEY or not PUBLIC_KEY:
        init_logger(message="Private/Public key not loaded properly", level="critical")
        raise RuntimeError("Private/Public key not loaded properly")
    
except Exception as e:
    init_logger(message=f"Error loading private/public keys: {str(e)}", level="critical")
    raise RuntimeError("Failed to initialize JWT keys") from e

async def create_access_token(user) -> str:
    try:
        access_exp_time = config.ACCESS_TOKEN_EXPIRE_MINUTES

        init_logger(message="Creating Access Jwt...")

        if not access_exp_time:
            init_logger(message="Could not able to fetch access token expiration time", level="warning")

        access_exp_time = current_time() + timedelta(minutes=access_exp_time)

        payload = {
            "email_ID": user.email_ID,
            "current_time": int(current_time().timestamp()),
            "exp": int(access_exp_time.timestamp()),
            "type": "access"
        }
        
        access_token = jwt.encode(header=config.JWT_HEADER, payload=payload, key=PRIVATE_KEY)

        if isinstance(access_token, bytes):
            access_token = access_token.decode('utf-8')

        init_logger(message=f"Access Token generated successfully for {user.email_ID}, Expiration: {access_exp_time}")

        return access_token
    
    except ValueError as ve:
        init_logger(message=f"ValueError in create_access_token: {str(ve)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Access Token generation configuration error"
        )

    except JoseError as je:
        init_logger(message=f"error creating access token {str(je)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    except Exception as e:
        init_logger(message=f"Unexpected error in create_access_token: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error generating access token"
        )


async def create_refresh_token(user) -> str:
    try:
        refresh_exp_time = config.REFRESH_TOKEN_EXPIRE_MINUTES

        init_logger(message="Creating Refresh Jwt...")

        if not refresh_exp_time:
            init_logger(message="Could not able to fetch refresh token expiration time", level="warning")

        refresh_exp_time = current_time() + timedelta(minutes=refresh_exp_time)

        payload = {
            "email_ID": user.email_ID,
            "current_time": int(current_time().timestamp()),
            "exp": int(refresh_exp_time.timestamp()),
            "type": "refresh"
        }
        
        refresh_token = jwt.encode(header=config.JWT_HEADER, payload=payload, key=PRIVATE_KEY)

        if isinstance(refresh_token, bytes):
            refresh_token = refresh_token.decode('utf-8')

        init_logger(message=f"Refresh token generated successfully for {user.email_ID}, Expiration: {refresh_exp_time}")

        refresh_token_db = Tokens(
            email_ID=user.email_ID,
            token=refresh_token,
            token_type=TokenType.REFRESH,
            expires_at=refresh_exp_time
        )

        await refresh_token_db.insert()

        return refresh_token
    
    except ValueError as ve:
        init_logger(message=f"ValueError in create_refresh_token: {str(ve)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Refresh Token generation configuration error"
        )

    except JoseError as je:
        init_logger(message=f"error creating refresh token {str(je)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    except Exception as e:
        init_logger(message=f"Unexpected error in create_refresh_token: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error generating Refresh token"
        )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.VITE_LOGIN_EP)

async def verify_n_refresh_token(request: Request) -> str:
    try:
        access_token = get_cookies_token(request=request)
        
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

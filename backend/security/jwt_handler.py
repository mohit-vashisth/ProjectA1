import token
from backend.core import config
from backend.schemas.blacklist_token_schema import BlacklistToken
from backend.utils.logger import init_logger
from backend.utils.current_time import current_time

from authlib.jose import jwt, JoseError
from fastapi import HTTPException, Depends, Security, status
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
        exp_time = config.ACCESS_TOKEN_EXPIRE_MINUTES

        init_logger(message="Creating Jwt...")

        if not exp_time:
            init_logger(message="Could not able to fetch expiration time", level="warning")

        exp_time = current_time() + timedelta(minutes=exp_time)

        payload = {
            "email_ID": user.email_ID,
            "current_time": int(current_time().timestamp()),
            "exp": int(exp_time.timestamp()),
            "type": "access"
        }
        
        jwt_token = jwt.encode(header=config.JWT_HEADER, payload=payload, key=PRIVATE_KEY)

        if isinstance(jwt_token, bytes):
            jwt_token = jwt_token.decode('utf-8')

        init_logger(message=f"Token generated successfully for {user.email_ID}, Expiration: {exp_time}")

        return jwt_token
    
    except ValueError as ve:
        init_logger(message=f"ValueError in create_access_token: {str(ve)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token generation configuration error"
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
            detail="Unexpected error generating token"
        )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.VITE_LOGIN_EP)

async def verify_n_refresh_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        if not isinstance(token, str):
            init_logger(message="Invalid token format received", level="warning")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                  detail="Invalid token format"
            )
        
        payload = jwt.decode(token, PUBLIC_KEY, claims_options={
            "exp": {"essential": True},
            "email_ID": {"essential": True},
            "type": {"essential": True}
        })

        init_logger(message="Verifying jwt token")

        payload.validate()

        if payload["type"] != "access":
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

        init_logger(message="Verified jwt token")

        return payload
    
    except JoseError as je:
        init_logger(message=f"JoseError in verify_access_token: {str(je)}", level="error")

        if "exp" in str(je):
            init_logger(message="Token expired, generating new token")

            try:
                expired_payload = jwt.decode(token, PUBLIC_KEY, validate=False)
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
    
async def check_blacklisted_token(token:str = Security(verify_n_refresh_token)):
    blacklisted = BlacklistToken.find_one({"token":token})
    if blacklisted:
        init_logger(message="The token is blacklisted.", level = "error")
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Token has beens blacklisted. Please login again"
        )
    return token

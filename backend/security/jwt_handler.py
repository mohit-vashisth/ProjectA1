from backend.core import config
from backend.utils.logger import init_logger
from backend.utils.current_time import current_time

from authlib.jose import jwt, JoseError
from fastapi import HTTPException, Depends, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer

try:
    PRIVATE_KEY, PUBLIC_KEY = config.read_pv_key()
    if not PRIVATE_KEY or not PUBLIC_KEY:
        init_logger(message="Private/Public key not loaded properly", level="critical")
        raise ValueError("Private/Public key not loaded properly")
except Exception as e:
    init_logger(message=f"Error loading private/public keys: {str(e)}", level="critical")
    raise

async def create_access_token(user):
    try:
        exp_time = current_time() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

        payload = {
            "email_ID": user.email_ID,
            "current_time": int(current_time().timestamp()),
            "exp": int(exp_time.timestamp()),
        }
        
        jwt_token = jwt.encode(header=config.JWT_HEADER, payload=payload, key=PRIVATE_KEY)

        if isinstance(jwt_token, bytes):
            jwt_token = jwt_token.decode('utf-8')

        init_logger(message=f"Token generated successfully for {user.email_ID}, Expiration: {exp_time}")

        return jwt_token
    except JoseError as je:
        init_logger(message=f"error creating access token {str(je)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token or Expired"
        )
    except Exception as e:
        init_logger(message=f"Unexpected error in create_access_token: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while generating token"
        )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.VITE_LOGIN_EP)

async def verify_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, PUBLIC_KEY, claims_options={
        "exp": {"essential": True},  # Ensures token has an expiry
        "email_ID": {"essential": True},  # Ensures token contains user_id
        })

        payload.validate()

        init_logger(message="Access token is valid")

        return payload
    
    except JoseError as je:
        init_logger(message=f"error verifying token: {str(je)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token or Expired"
        )
    except Exception as e:
        init_logger(message=f"Unexpected error in create_access_token: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while generating token"
        )

async def refresh_access_token():
    pass
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
        raise RuntimeError("Private/Public key not loaded properly")
    
except Exception as exp_err:
    init_logger(message=f"Error loading private/public keys: {str(exp_err)}", level="critical")
    raise RuntimeError("Failed to initialize JWT keys") from exp_err

async def create_access_token(user):
    try:
        if not config.ACCESS_TOKEN_EXPIRE_MINUTES:
            init_logger(message="Could not able to fetch expiration time", level="error")

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

async def verify_n_refresh_token(token: str = Depends(oauth2_scheme)):
    try:

        if not isinstance(token, str):
            init_logger(message="Invalid token format received", level="error")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                  detail="Invalid token format"
            )
        
        payload = jwt.decode(token, PUBLIC_KEY, claims_options={
        "exp": {"essential": True},  # Ensures token has an expiry
        "email_ID": {"essential": True},  # Ensures token contains user_id
        })

        try:
            payload.validate()

        except JoseError as ve:
            init_logger(message=f"Validation error in verify_access_token: {str(ve)}", level="error")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims"
            )

        init_logger(message=f"Token validated successfully for {payload['email_ID']}")

        return payload
    
    except JoseError as je:
        init_logger(message=f"JoseError in verify_access_token: {str(je)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    except Exception as e:
        init_logger(message=f"Unexpected error in verify_access_token: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while verifying token"
        )
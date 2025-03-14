from backend.core import config
from backend.schemas.token_scema import TokenType, Tokens
from backend.security.token_utils import create_payload, get_token_exp_time, token_encode
from backend.utils.logger import init_logger

from authlib.jose import jwt, JoseError
from fastapi import HTTPException, Request, status
from datetime import timedelta


async def create_access_token(user) -> str:
    try:
        init_logger(message="Creating Access Jwt...")

        access_exp_time = get_token_exp_time(token_type="access")

        payload = create_payload(email_id=user.email_ID, expiry_time=access_exp_time, token_type="access")
        
        access_token = token_encode(payload=payload)

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
        init_logger(message="Creating Refresh Jwt...")

        refresh_exp_time = get_token_exp_time(token_type="refresh")
        
        payload = create_payload(email_id=user.email_ID, expiry_time=refresh_exp_time, token_type="refresh")
        
        refresh_token = token_encode(payload=payload)

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


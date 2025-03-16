from backend.core import config
from backend.schemas.token_schema import TokenType, Tokens
from backend.utils.logger import init_logger
from backend.utils.current_time import current_time
from backend.utils.load_keys import load_keys

from authlib.jose import jwt
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Any


PRIVATE_KEY, _ = load_keys()

def exp_time(token_type: str = "access"):
    return (current_time() + timedelta(seconds=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60 if token_type.lower() == "access" else config.REFRESH_TOKEN_EXPIRE_MINUTES * 60))

def create_payload(email_id: str, expiry_time: datetime, token_type: str)-> dict[str, Any]:
    return {
        "email_ID":email_id,
        "current_time": int(current_time().timestamp()),
        "exp": expiry_time,
        "type": token_type
    }

def token_encode(payload) -> str:
    token = jwt.encode(header= config.JWT_HEADER, payload=payload, key=PRIVATE_KEY)
    return token.decode('utf-8') if isinstance(token, bytes) else token


async def create_access_token(user) -> str:
    try:
        init_logger(message="Creating Access Jwt...")

        payload = create_payload(email_id=user.email_ID, expiry_time=exp_time(), token_type="access")
        
        access_token = token_encode(payload=payload)

        init_logger(message=f"Access Token generated successfully for {user.email_ID}, Expiration: {exp_time()}")

        return access_token
    
    except Exception as e:
        init_logger(message=f"Unexpected error in create_access_token: {str(e)}", level="critical")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error generating access token"
        )


async def create_refresh_token(user) -> str:
    try:
        init_logger(message="Creating Refresh Jwt...")

        payload = create_payload(email_id=user.email_ID, expiry_time=exp_time(token_type="refresh"), token_type="refresh")
        
        refresh_token = token_encode(payload=payload)

        init_logger(message=f"Refresh token generated successfully for {user.email_ID}, Expiration: {exp_time(token_type='refresh')}")

        refresh_token_db = Tokens(
            email_ID=user.email_ID,
            token=refresh_token,
            token_type=TokenType.REFRESH,
            expires_at=exp_time(token_type='refresh')
        )

        await refresh_token_db.insert()

        return refresh_token
    
    except Exception as e:
        init_logger(message=f"Unexpected error in create_refresh_token: {str(e)}", level="critical")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error generating Refresh token"
        )


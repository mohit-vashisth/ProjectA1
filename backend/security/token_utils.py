
from datetime import datetime, timedelta
from typing import Any
from authlib.jose import jwt
from fastapi import HTTPException, status
from pydantic import EmailStr
from backend.core import config
from backend.utils.current_time import current_time
from backend.utils.load_keys import load_keys
from backend.utils.logger import init_logger

PRIVATE_KEY, _ = load_keys()

def create_payload(email_id: EmailStr, expiry_time: datetime, token_type: str)-> dict[str, Any]:
    return {
        "email_ID":email_id,
        "current_time": int(current_time().timestamp()),
        "exp": expiry_time,
        "type": token_type
    }

def get_token_exp_time(token_type: str):
    if token_type == "access":
        access_exp_time = config.ACCESS_TOKEN_EXPIRE_MINUTES
        
        if not access_exp_time:
            init_logger(message="Could not fetch access token expiration time", level="warning")

        return current_time() + timedelta(minutes=access_exp_time)
    elif token_type == "refresh":
        refresh_exp_time = config.REFRESH_TOKEN_EXPIRE_MINUTES

        if not refresh_exp_time:
            init_logger(message="Could not able to fetch refresh token expiration time", level="warning")

        return current_time() + timedelta(minutes=refresh_exp_time)
    
    else:
        init_logger(message="Incorrect token type.", level="warning")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect token type"
        )

def token_encode(payload) -> str:
    token = jwt.encode(header= config.JWT_HEADER, payload=payload, key=PRIVATE_KEY)
    return token.decode('utf-8') if isinstance(token, bytes) else token
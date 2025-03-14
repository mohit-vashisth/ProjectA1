
from fastapi import HTTPException, status
from backend.security.jwt_handler import check_blacklisted_token
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
from authlib.jose import jwt, JoseError
from fastapi import HTTPException, Depends
from backend.auth.create_user import create_user
from backend.core import config
from backend.utils.current_time import current_time
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
import logging

PRIVATE_KEY, PUBLIC_KEY = config.read_pv_key()

async def create_access_token(user):
    exp_time = current_time() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "email_ID": user.email_ID,
        "current_time": int(current_time().timestamp()),
        "exp": int(exp_time.timestamp()),
    }
    jwt_token = jwt.encode(header=config.JWT_HEADER, payload=payload, key=PRIVATE_KEY)
    logging.info("Token generated sucessfully")
    return jwt_token.decode('utf-8')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.VITE_LOGIN_EP)

async def verify_access_token(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, PUBLIC_KEY, claims_options={
    "exp": {"essential": True},  # Ensures token has an expiry
    "email_ID": {"essential": True},  # Ensures token contains user_id
    })
    payload.validate()
    return payload



async def refresh_access_token():
    pass
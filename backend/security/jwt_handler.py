from authlib.jose import jwt
from authlib.jose.errors import JoseError
from auth.create_user import create_user
from core import config
from utils.current_time import current_time
from datetime import timedelta

private_key, public_key = config.read_pv_key()

async def create_access_token(user):
    user_info = await create_user(user)
    exp_time = current_time() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    Payload = {
        "email_ID": user_info.email_ID,
        "current_time": current_time(),
        "exp": exp_time,
    }
    jwt_token = jwt.encode(header=config.JWT_HEADER, payload=Payload, key=private_key)
    return jwt_token

async def verify_access_token():
    pass

async def refresh_access_token():
    pass
from authlib.jose import jwt
from authlib.jose.errors import JoseError
from auth.create_user import create_user
from core import config

async def create_access_token(user):
    user_info = await create_user(user)
    # user_info = user_info.dict()
    jwt_token = await jwt.encode(dict(user_info), config.read_pv_key(), config.JWT_ALGORITHM)

    return jwt_token

async def verify_access_token():
    pass

async def refresh_access_token():
    pass
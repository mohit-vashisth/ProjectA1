from backend.core import config
from fastapi.responses import JSONResponse
from backend.utils.logger import init_logger
from backend.auth.create_user import create_user
from backend.schemas.user_schema import UserSignup
from backend.security.create_jwt import create_access_token
from backend.security.check_existing_email import check_existing_email

from fastapi import APIRouter, Request, Response, status

signup_route = APIRouter()
@signup_route.post(path=config.SIGNUP_EP, status_code=status.HTTP_201_CREATED)
async def signup(user_info: UserSignup, response: Response, request: Request):
    init_logger(message=f"signup attemp for email {user_info.email_ID}", request=request)

    await check_existing_email(req_email=user_info.email_ID)

    user = await create_user(user_info=user_info)

    access_token = await create_access_token(user=user)

    init_logger(message=f"user created in database: A_token -> {access_token[:6]}")
    
    tokens = {
        "access_token": access_token,
    }

    response = JSONResponse(
        content= {
            "message": "User logged in successfully.",
            "userName": user_info.user_name,
            "userEmail": user_info.email_ID
        },
        headers={"X-API-Version": config.APP_VERSION, "Content-Type": "application/json", **response.headers},
    )

    for key, value in tokens.items():
        max_age = config.ACCESS_TOKEN_EXPIRE_MINUTES * 60 if key == "access_token" else config.REFRESH_TOKEN_EXPIRE_MINUTES * 60
        response.set_cookie(
            key=key,
            value=value,
            httponly=True,
            secure=not config.DEBUG,
            samesite="lax",
            max_age=max_age,
            path="/"
        )

    return response
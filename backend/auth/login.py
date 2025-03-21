from backend.core import config
from backend.utils.logger import init_logger
from backend.schemas.user_schema import User_login
from backend.auth.signup import create_access_token
from backend.database.queries.user_queries import get_user
from backend.security.create_jwt import create_refresh_token
from backend.security.pass_verifier import verify_user_password

from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Request, Response, status

login_route = APIRouter()

@login_route.post(path=config.VITE_LOGIN_EP, status_code=status.HTTP_200_OK)
async def login(user_info: User_login, request: Request, response: Response):
    init_logger(message=f"Login attemp for email {user_info.email_ID}", request=request)
    
    user_data = await get_user(req_email=user_info.email_ID)

    if user_data is None:
        init_logger(message=f"User not found: {user_info.email_ID}", level="warning", request=request)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User: {user_info.email_ID} not found"
        )
    
    verify_user_password(hashed_password=user_data.auth.password, password=user_info.password)
    
    access_token = await create_access_token(user=user_data)
    refresh_token = await create_refresh_token(user=user_data)

    init_logger(message=f"User {user_info.email_ID} logged in successfully", request=request)

    tokens = {
        "access_token": access_token,
    }

    response = JSONResponse(
        content= {
            "message": "User logged in successfully.",
            "userName": user_data.profile.user_name,
            "userEmail": user_data.email_ID
        },
        headers={"X-API-Version": config.APP_VERSION, "Content-Type": "application/json", **response.headers},
    )
    
    for key, value in tokens.items():
        max_age = config.ACCESS_TOKEN_EXPIRE_MINUTES * 60 if key == "access_token" else config.REFRESH_TOKEN_EXPIRE_MINUTES  * 60
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
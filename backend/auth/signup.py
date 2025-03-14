from fastapi.responses import JSONResponse
from backend.schemas.user_schema import User_signup
from backend.core import config
from backend.security.check_existing_email import check_existing_email
from backend.auth.create_user import create_user
from backend.security.jwt_handler import create_access_token, create_refresh_token
from backend.utils.logger import init_logger

from fastapi import APIRouter, HTTPException, Response, status

signup_route = APIRouter()
@signup_route.post(path=config.VITE_SIGNUP_EP, status_code=status.HTTP_201_CREATED)
async def signup(user_info: User_signup, response: Response):
    try:
        init_logger(message=f"signup attemp for email {user_info.email_ID}")

        await check_existing_email(req_email=user_info.email_ID)

        user = await create_user(user_info=user_info)

        access_token = await create_access_token(user=user)
        refresh_token = await create_refresh_token(user=user)


        init_logger(message=f"user created in database: token -> {access_token}", level="critical")
        
        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        for key, value in tokens.items():
            response.set_cookie(
                key=key,
                value=value,
                httponly=True,
                secure=not config.DEBUG,
                samesite="lax",
                max_age=600 if config.DEBUG else 86400
            )

        return JSONResponse(
            content= {
                "message": "User logged in successfully.",
                "userName": user_info.user_name,
                "userEmail": user_info.email_ID
            },
            headers={"X-API-Version": config.APP_VERSION, **response.headers}
        )
    
    except Exception as e:
        init_logger(message=f"Error during signup: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="something went wrong"
        )

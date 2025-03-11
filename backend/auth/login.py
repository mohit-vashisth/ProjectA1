from backend.auth.signup import create_access_token
from backend.schemas.user_schema import User_login
from backend.security.pass_verifier import verify_user_password
from backend.database.queries.user_queries import get_user
from backend.core import config
from backend.utils.logger import init_logger
from backend.core import config

from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse

login_route = APIRouter()

@login_route.post(path=config.VITE_LOGIN_EP, status_code=status.HTTP_200_OK)
async def login(user_info: User_login, response: Response, request: Request):
    try:
        init_logger(message=f"Login attemp for email {user_info.email_ID}", request=request)
        
        user_data = await get_user(req_email=user_info.email_ID)

        if user_data is None:
            init_logger(message=f"User not found: {user_info.email_ID}", level="error", request=request)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        verify_user_password(hashed_password=user_data.auth.password, password=user_info.password)
        
        access_token = await create_access_token(user=user_data)

        init_logger(message=f"User {user_info.email_ID} logged in successfully", request=request)

        response.set_cookie(
            key = "access_token",
            value = access_token,
            httponly=True,
            secure=not config.DEBUG,
            samesite="lax",
            max_age=600 if config.DEBUG else 86400
        )

        return JSONResponse(
            content= {
                "message": "User logged in successfully.",
                "userName": user_data.profile.user_name,
                "userEmail": user_data.email_ID
            },
            headers={"X-API-Version": config.APP_VERSION, **response.headers}
        )

    except HTTPException as http_exp:
        init_logger(message=f"Unexpected Error during login: {str(http_exp)}", level="error", request=request)
        raise http_exp
    
    except Exception as exp:
        init_logger(message=f"Unexpected Error during login: {str(exp)}", level="error", request=request)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong. Please try again later."
        )
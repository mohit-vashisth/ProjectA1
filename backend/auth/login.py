from backend.auth.signup import create_access_token
from backend.schemas.user_model import Users
from backend.schemas.user_schema import User_login
from backend.security.pass_verifier import verify_user_password
from backend.database.user_queries import get_user
from backend.core import config
from backend.utils.logger import init_logger

from fastapi import APIRouter, HTTPException, Response, status

login_route = APIRouter()

@login_route.post(path=config.VITE_LOGIN_EP, status_code=status.HTTP_200_OK)
async def login(user_info: User_login, response: Response):
    try:
        init_logger(message=f"Login attemp for email {user_info.email_ID}")
        
        user_data: Users = await get_user(req_email=user_info.email_ID)
        
        verify_user_password(hashed_password=user_data.password, password=user_info.password)
        
        access_token = await create_access_token(user=user_data)

        init_logger(message=f"User {user_info.email_ID} logged in successfully")

        response.set_cookie(
            key = "access_token",
            value = access_token,
            httponly=True,
            #secure=True,
            samesite=None,
            max_age=86400
        )

        return {
        "message": "User logged in successfully.",
        "userName": user_data.user_name,
        "userEmail": user_data.email_ID
        }
    
    except Exception as exp:
        init_logger(message=f"Unexpected Error during login: {str(exp)}", level="critical")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error")
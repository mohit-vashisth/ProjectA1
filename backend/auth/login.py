from backend.auth.signup import create_access_token
from backend.schemas.user_model import Users
from backend.schemas.user_schema import User_login
from backend.security.check_existing_email import check_existing_email
from backend.security.pass_verifier import verify_user_password
from backend.database.user_queries import get_user
from backend.core import config
from backend.utils.logger import init_logger

from fastapi import APIRouter, HTTPException, status

login_route = APIRouter()

@login_route.post(path=config.VITE_LOGIN_EP, status_code=status.HTTP_200_OK)
async def login(user_info: User_login):
    try:
        init_logger(message=f"Login attemp for email {user_info.email_ID}")

        if not user_info.email_ID:
            init_logger(message="Login failed: Email missing", level="warning")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email required"
            )
        if not user_info.password:
            init_logger(message=f"Login failed: password Missing", level="warning")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password required"
            )
        
        user_data: Users | None = await get_user(req_email=user_info.email_ID)
        
        if user_data is None:
            init_logger(message=f"Login failed for {user_info.email_ID}: User not found", level="warning")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        try:
            is_valid_password = verify_user_password(hashed_password=user_data.password, password=user_info.password)
        except Exception as pass_err:
            init_logger(message=f"Error verifying password for {user_info.email_ID}: {str(pass_err)}", level="error")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error verifying password"
            )
        
        if not is_valid_password:
            init_logger(message=f"Login failed for {user_info.email_ID}: Invalid password", level="warning")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )
        
        access_token = await create_access_token(user=user_data)

        init_logger(message=f"User {user_info.email_ID} logged in successfully")

        return {
        "message": "User logged in successfully.",
        "access_token": access_token
        }
    except HTTPException as http_exp:
        init_logger(message=f"HTTP Exception: {http_exp.detail}", level="error")
        raise http_exp
    except Exception as exp:
        init_logger(message=f"Unexpected Error during login: {str(exp)}", level="critical")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error")
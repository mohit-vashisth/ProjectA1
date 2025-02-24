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
            init_logger(message=f"Login failed: Email missing {user_info.email_ID}", level="warning")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email required"
            )
        if not user_info.password:
            init_logger(message=f"Login failed: password Missing {user_info.password}", level="warning")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password required"
            )
        
        await check_existing_email(req_email=user_info.email_ID, is_signup=False)

        user_data: Users | None = await get_user(req_email=user_info.email_ID)
        
        if user_data is None:
            init_logger(message=f"Login failed for {user_info.email_ID}: User not found", level="warning")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not verify_user_password(hashed_password=user_data.password, password=user_info.password):
            init_logger(message=f"Login failed for {user_info.email_ID}: Invalid password", level="warning")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
        )
        else:
            init_logger(f"User {user_info.email_ID} logged in successfully", "info")

        return {
        "message": "User logged in successfully.",
        "access_token": "sampleAccessToken"
        }
    except HTTPException as http_exp:
        init_logger(message=f"HTTP Exception: {http_exp.detail}", level="error")
        raise http_exp
    except Exception as exp:
        init_logger(message=f"Unexpected Error during login: {str(exp)}", level="critical")
        raise HTTPException(status_code=500, detail="Internal Server Error")
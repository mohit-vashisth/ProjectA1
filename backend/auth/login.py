from fastapi import APIRouter, HTTPException, status
from schemas.user_model import Users
from schemas.user_schema import User_login
from security.pass_verifier import verify_user_password
from security.check_existing_email import check_existing_email
from core import config
from database.user_queries import get_user
from schemas.log_schema import logging

login_route = APIRouter()

@login_route.post(path=config.VITE_LOGIN_EP, status_code=status.HTTP_200_OK)
async def login(user_info: User_login):
    try:
        if not user_info.email_ID:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email required"
            )
        if not user_info.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password required"
            )
        await check_existing_email(req_email=user_info.email_ID, is_signup=False)

        user_data: Users | None = await get_user(req_email=user_info.email_ID)  # First, await the function call
        if user_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if not verify_user_password(hashed_password=user_data.password, password=user_info.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
        )
        else:
            print(f"user {user_info} is verified and logged in") # temperory

        return {
        "message": "User logged in successfully.",
        "access_token": "sampleAccessToken"
        }
    except HTTPException as http_exp:
        raise http_exp
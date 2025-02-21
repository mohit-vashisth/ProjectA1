from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import User_login
from security.pass_verifier import verify_user_password
from security.check_existing_email import check_existing_email
from core import config
from database.user_queries import get_user
import logging

login_route = APIRouter()

@login_route.post(config.VITE_LOGIN_EP, status_code=status.HTTP_200_OK)
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
        await check_existing_email(user_info.email_ID, False)

        user_data = await get_user(user_info.email_ID)  # First, await the function call
        if user_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if not verify_user_password(user_data.password, user_info.password):
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
        pass
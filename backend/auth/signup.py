from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import User_signup
from core import config
from security.check_existing_email import check_existing_email
from auth.create_user import create_user
from security.jwt_handler import create_access_token

signup_route = APIRouter()
# signup route/path/Endpoint
@signup_route.post(config.VITE_SIGNUP_EP, status_code=status.HTTP_201_CREATED)
async def signup(user_info: User_signup):
    if not user_info.user_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name required"
        )
    if not user_info.email_ID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email required"
        )
    if not user_info.contact_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contact Number required"
        )
    if not user_info.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password required"
        )

    if await check_existing_email(user_info.email_ID, True):
        print("JWT token:", await create_access_token(user_info))
    
    return {
    "message": "User signed up successfully",
    "userName": user_info.user_name,
    "userEmail": user_info.email_ID,
    "access_token": "sampleAccessToken"
}

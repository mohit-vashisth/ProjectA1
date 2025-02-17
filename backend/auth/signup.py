from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import User_signup
from core.config import env_variables
from security.check_existing_email import check_existing_email
from auth.create_user import create_user

signup_route = APIRouter()

print(env_variables("VITE_SIGNUP_EP"))
# signup route/path/Endpoint
@signup_route.post(env_variables("VITE_SIGNUP_EP"), status_code=status.HTTP_201_CREATED)
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
        await create_user(user_info)
    
    return {
    "message": "User signed up successfully",
    "userName": user_info.user_name,
    "userEmail": user_info.email_ID,
    "access_token": "sampleAccessToken"
}
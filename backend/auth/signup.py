import re
from fastapi import APIRouter, HTTPException, status
from schema.user_model import User_signup
from database.user_storage import set_user_info, get_user_info, database_emails

signup_route = APIRouter()

# Function to validate email format
async def emailValidation(email: str):
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

# Handling existing user email ids
async def check_existing_email(emails: set, requested_email: str):
    if requested_email in emails:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already in use"
        )


# signup route/path/Endpoint
@signup_route.post("/signup", status_code=status.HTTP_201_CREATED)
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
    if not user_info.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password required"
        )
    await emailValidation(user_info.email_ID)
    await check_existing_email(database_emails(), user_info.email_ID)

    set_user_info(user_info)

    print("Received signup data:", get_user_info())

    return {
    "message": "User signed up successfully",
    "userName": user_info.user_name,
    "userEmail": user_info.email_ID,
    "accessToken": "m35"
}


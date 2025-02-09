from fastapi import APIRouter, HTTPException, status
from schema.user_model import User_login
from security.security import verify_user_password
from database.user_storage import database_emails
from security.email_verification import email_validation
from security.check_existing_email import check_existing_email
from config import env_variables

login_route = APIRouter()
user_hashed_pass = "$argon2id$v=19$m=65536,t=3,p=4$GUPofc+Zs7aWcs55j/F+rw$nmfo/+hbdiPI/eBZnezGm4v10dP0imqpaB2Q56f43gc"

@login_route.post(env_variables("VITE_LOGIN_EP"), status_code=status.HTTP_200_OK)
async def login(user_info: User_login):
    print(env_variables("VITE_LOGIN_EP"))
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
    
    await email_validation(user_info.email_ID)
    if not await check_existing_email(database_emails(),user_info.email_ID, False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account not found associated with this email id"
        )
    if not verify_user_password(user_info.password, user_hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Invalid password"
              )

    return {
    "message": "User logged in successfully.",
    "access_token": "sampleAccessToken"
    }

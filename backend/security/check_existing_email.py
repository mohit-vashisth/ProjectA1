from fastapi import HTTPException, status
from backend.schemas.user_model import Users
from backend.database.user_queries import get_user
import logging

async def check_existing_email(req_email: str, is_signup: bool = True) -> bool:
    user_data: Users | None = await get_user(req_email=req_email)
    if user_data:
        logging.info(msg=f"User found for Email: {user_data}") #debugg
    else:
        logging.error(msg=f"User not found for Email: {user_data}") #debugg

    if is_signup and user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already in use"
        )
    
    if not is_signup and not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account found with this email"
        )
    
    return True

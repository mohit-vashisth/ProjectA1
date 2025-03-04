from fastapi import HTTPException, status
from backend.database.connection import Users
from backend.utils.logger import init_logger

async def get_user(req_email: str) -> Users:
    try:
        user_data = await Users.find_one(Users.email_ID == req_email)
        if user_data is None:
            init_logger(message=f"User not found: {req_email}", level="error")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        init_logger(message=f"User info for email id: {req_email} found in DB")
        return user_data
    
    except Exception as e:
        init_logger(message=f"Something went wrong: {e}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )
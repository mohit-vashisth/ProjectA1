from fastapi import HTTPException, status
from backend.database.connection import Users
from backend.utils.logger import init_logger

async def get_user(req_email: str) -> Users | None:
    try:
        user_data: Users | None = await Users.find_one(Users.email_ID == req_email)
        init_logger(message=f"user info:{user_data}")
        return user_data
    except HTTPException as http_exp:
        init_logger(message=f"Error getting User info: {http_exp}", level="error")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        init_logger(message=f"Something went wrong: {e}", level="error")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Something went wrong"
        )
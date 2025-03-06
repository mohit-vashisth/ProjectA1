from fastapi import HTTPException, status
from backend.database.connection import Users
from backend.utils.logger import init_logger

async def get_user(req_email: str) -> Users | None:
    try:
        user_data = await Users.find_one({"email" : req_email})
        if user_data is None:
            init_logger(message=f"User not found: {req_email}", level="error")
            return None
        init_logger(message=f"User info for email id: {req_email} found in DB")
        return user_data
    
    except Exception as e:
        err_type = type(e).__name__
        init_logger(message=f"Error while fetching user data: {err_type} : {e}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )
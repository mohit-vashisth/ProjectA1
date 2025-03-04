from fastapi import HTTPException, status
from backend.schemas.user_model import Users
from backend.database.user_queries import get_user
from backend.utils.logger import init_logger

async def check_existing_email(req_email: str) -> bool:
    try:
        init_logger(message=f"Checking if email exists: {req_email}")
        
        user_data: Users = await get_user(req_email=req_email)

        init_logger(message=f"Email ID: {req_email} is not registered. Proceeding with signup.")
        
        if user_data:
            init_logger(message=f"User found for Email: {req_email}, cannot proceed", level="warning")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already in use"
            )
    
        return True

    except HTTPException as http_exp:
        init_logger(message=f"HTTP Exception while checking email: {http_exp.detail}", level="error")
        raise http_exp  # Re-raise the specific HTTPException

    except Exception as e:
        init_logger(message=f"Unexpected error while fetching user with email {req_email}: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error while checking email"
        )

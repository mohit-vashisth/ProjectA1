from backend.utils.logger import init_logger
from backend.database.queries.user_queries import get_user

from fastapi import HTTPException, status

async def check_existing_email(req_email: str) -> bool:
    try:
        init_logger(message=f"Checking if email exists: {req_email}")
        
        user_data = await get_user(req_email=req_email)

        if user_data:
            init_logger(message=f"User found for Email: {req_email}, cannot proceed", level="warning")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already in use"
            )
    
        init_logger(message=f"Email ID: {req_email} is not registered. Proceeding with signup.")
        return True

    except HTTPException as http_exp:
        init_logger(message=f"HTTP Exception while checking email: {http_exp.detail}", level="error")
        raise http_exp

    except Exception as e:
        init_logger(message=f"Unexpected error while fetching user with email {req_email}: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error while checking email"
        )

from fastapi import HTTPException, status
from backend.schemas.user_model import Users
from backend.database.user_queries import get_user
from backend.utils.logger import init_logger

async def check_existing_email(req_email: str) -> bool:
    user_data: Users | None = await get_user(req_email=req_email)

    if user_data:
        init_logger(message=f"User found for Email: {req_email}", level="warning")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already in use"
        )
    
    return True

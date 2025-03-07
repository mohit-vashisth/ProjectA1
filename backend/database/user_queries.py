from fastapi import HTTPException, status
import pymongo.errors
from backend.database.connection import Users
from backend.utils.logger import init_logger

async def get_user(req_email: str) -> Users | None:
    try:
        user_data = await Users.find_one({"email_ID" : req_email})
        if user_data is None:
            init_logger(message=f"User not found: {req_email}", level="info")
            return None
        init_logger(message=f"User info for email id: {req_email} found in DB")
        return user_data
    
    except pymongo.errors.ServerSelectionTimeoutError as e:
        init_logger(message=f"Database connection error: {type(e).__name__} : {e}", level="critical")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable"
        )

    except pymongo.errors.OperationFailure as e:
        init_logger(message=f"MongoDB operation failure: {type(e).__name__} : {e}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )

    except Exception as e:
        init_logger(message=f"Unexpected error while fetching user data: {type(e).__name__} : {e}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )
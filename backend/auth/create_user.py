from backend.schemas.user_model import Auth, UserProfile, Users
from backend.security.pass_hasher import password_hash
from pymongo.errors import PyMongoError
from pydantic import ValidationError
from fastapi import HTTPException, status

from backend.utils.logger import init_logger

async def create_user(user_info) -> Users:
    try:
        init_logger(message=f"Creating user in database for user ID: {user_info.email_ID}")

        user = Users(
            email_ID=user_info.email_ID,
            profile = UserProfile(
                user_name=user_info.user_name,
                contact_number=user_info.contact_number
            ),
            auth=Auth(
                password=password_hash(password=user_info.password),
            ),
            is_Premium=False,
            privacy_link=user_info.privacy_link
        )
        
        await user.insert()
        
        init_logger(message="User Created in Database")
        return user

    except ValidationError as val_err:
        init_logger(message=f"Validation Error: {str(val_err)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid user data provided"
        )

    except PyMongoError as db_err:
        init_logger(message=f"Database Error: {str(db_err)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

    except Exception as e:
        init_logger(message=f"Unexpected Error: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

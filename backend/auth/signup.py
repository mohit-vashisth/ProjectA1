from backend.schemas.user_schema import User_signup
from backend.core import config
from backend.security.check_existing_email import check_existing_email
from backend.auth.create_user import create_user
from backend.schemas.log_schema import logger
from backend.security.jwt_handler import create_access_token
from backend.utils.logger import init_logger

from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, status

signup_route = APIRouter()
# signup route/path/Endpoint
@signup_route.post(path=config.VITE_SIGNUP_EP, status_code=status.HTTP_201_CREATED)
async def signup(user_info: User_signup):
    try:
        init_logger(message=f"signup attemp for email {user_info.email_ID}")

        await check_existing_email(req_email=user_info.email_ID)

        user = await create_user(user_info=user_info)
        if not user:
            init_logger(message=f"unable to create user in database")
        
        init_logger(message=f"user created in database")

        access_token = await create_access_token(user=user)

        init_logger(message=f"user created in database")

        return {
                "message": "User signed up successfully",
                "userName": user_info.user_name,
                "userEmail": user_info.email_ID,
                "access_token": access_token
            }
    
    except ConnectionError as cnn_error:
        init_logger(message=f"Database Connection Error: {cnn_error}", level="error")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unable to connect to database."
        )
    except HTTPException as http_except:
        init_logger(message=f"Http exception: {str(http_except)}", level="error")
        raise http_except
    except Exception as e:
        init_logger(message=f"Error during signup: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="something went wrong"
        )

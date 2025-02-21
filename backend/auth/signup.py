from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import User_signup
from core import config
from security.check_existing_email import check_existing_email
from auth.create_user import create_user
from security.jwt_handler import create_access_token
from fastapi.responses import JSONResponse
from schemas.log_schema import logger

signup_route = APIRouter()
# signup route/path/Endpoint
@signup_route.post(config.VITE_SIGNUP_EP, status_code=status.HTTP_201_CREATED)
async def signup(user_info: User_signup):
    try:
        if not user_info.user_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Name required"
            )
        if not user_info.email_ID:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email required"
            )
        if not user_info.contact_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contact Number required"
            )
        if not user_info.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password required"
            )

        if await check_existing_email(user_info.email_ID, True):
            user = await create_user(user_info) # type: ignore
            logger.info("User creation sucessful")
            token = await create_access_token(user)

            logger.info("Signup sucessful") #debugg

            return JSONResponse(
                content={
                    "message": "User signed up successfully",
                    "userName": user_info.user_name,
                    "userEmail": user_info.email_ID,
                    "access_token": token
                },
                status_code=status.HTTP_201_CREATED
        )
    except ConnectionError as cnn_error:
        logger.error(f"Database Connection Error: {cnn_error}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unable to connect to database."
        )

    except HTTPException as http_except:
        logger.error(f"Http exception: {http_except}")
        raise http_except

    except Exception as e:
        logger.error(f"Error during signup: {e}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="something went wrong"
        )

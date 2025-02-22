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
@signup_route.post(path=config.VITE_SIGNUP_EP, status_code=status.HTTP_201_CREATED)
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

        if await check_existing_email(req_email=user_info.email_ID, is_signup=True):
            user = await create_user(user_info=user_info) # type: ignore
            logger.info(msg="User creation sucessful")
            token = await create_access_token(user=user)

            logger.info(msg="Signup sucessful") #debugg

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
        logger.error(msg=f"Database Connection Error: {cnn_error}") #debugg

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unable to connect to database."
        )

    except HTTPException as http_except:
        logger.error(msg=f"Http exception: {http_except}") #debugg
        raise http_except

    except Exception as e:
        logger.error(msg=f"Error during signup: {e}") #debugg

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="something went wrong"
        )

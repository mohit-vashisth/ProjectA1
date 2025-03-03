from backend.schemas.user_model import Users
from backend.security.pass_hasher import password_hash
from pymongo.errors import PyMongoError
from pydantic import ValidationError

from backend.utils.logger import init_logger

async def create_user(user_info) -> Users | None:
    try:
        user = Users(
            user_name=user_info.user_name,
            email_ID=user_info.email_ID,
            password=password_hash(password=user_info.password),
            time_zone=user_info.time_zone,
            privacy_link=user_info.privacy_link,
            contact_number=user_info.contact_number
        )
        await user.insert()
        return user

    except ValidationError as val_err:
        init_logger(message=f"Validation Error: {str(val_err)}", level="error")
        return None

    except PyMongoError as db_err:
        init_logger(message=f"Database Error: {str(db_err)}", level="error")
        return None

    except Exception as e:
        init_logger(message=f"Unexpected Error: {str(e)}", level="error")
        return None

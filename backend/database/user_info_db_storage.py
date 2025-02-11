from schema.user_models import User_db_model
from security.security import password_hash

async def create_user(user_info: dict) -> User_db_model:
    user = User_db_model(
        user_info.user_name,
        user_info.email_ID,
        password_hash(user_info.password),
        user_info.time_zone,
        user_info.privacy_link,
        user_info.contact_number
        )
    await user.insert()
    return user
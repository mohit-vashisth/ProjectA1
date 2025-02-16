from schemas.user_model import Users
from security.pass_hasher import password_hash

async def create_user(user_info: dict) -> Users:
    user = Users(
        user_name=user_info.user_name,
        email_ID=user_info.email_ID,
        password=password_hash(user_info.password),
        time_zone=user_info.time_zone,
        privacy_link=user_info.privacy_link,
        contact_number=user_info.contact_number
        )
    await user.insert()
    return user
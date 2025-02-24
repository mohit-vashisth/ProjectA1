from backend.database.connection import Users
from backend.utils.logger import init_logger

async def get_user(req_email: str) -> Users | None:
        user_data: Users | None = await Users.find_one(Users.email_ID == req_email)
        init_logger(message=f"user info:{user_data}")
        return user_data
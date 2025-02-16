from typing import Optional
from database.connection import Users

async def get_user(req_email: str) -> Optional[Users]:
    user_data = await Users.find_one(Users.email_ID == req_email)
    return user_data

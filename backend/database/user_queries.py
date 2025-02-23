from backend.database.connection import Users

async def get_user(req_email: str) -> Users | None:
        user_data: Users | None = await Users.find_one(Users.email_ID == req_email)
        return user_data
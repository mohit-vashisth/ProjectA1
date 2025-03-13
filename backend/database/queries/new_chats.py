from fastapi import HTTPException, status, Request, Response
from backend.database.queries.user_queries import get_user
from backend.schemas.chat_schema import Chats
from backend.security.jwt_data_extract import get_jwt_email
from backend.utils.logger import init_logger


async def create_new_chat(payload, request:Request):
    email_id = get_jwt_email(decoded_token=payload)
    
    user_data = await get_user(req_email=email_id)
    
    if user_data is None:
            init_logger(message=f"User not found: {email_id}", level="error", request=request)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    init_logger(message=f"user data: {user_data}", level="critical")

    chat_id = user_data.email_ID
    init_logger(message=f"get_attr: {chat_id}", level="critical")
    
    chat = Chats(
        chat_id="1",
        email_ID= email_id,
        chat_name="voice_chat"
    )

    await chat.insert()
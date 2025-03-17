import uuid
from fastapi import HTTPException, status, Request, Response
from backend.database.queries.user_queries import get_user
from backend.schemas.chat_schema import Chats
from backend.security.create_n_verify_chat_id import generate_chat_id, default_chat_name
from backend.security.jwt_data_extract import get_jwt_email
from backend.utils.logger import init_logger
from backend.utils.current_time import current_time
from beanie.exceptions import CollectionWasNotInitialized


async def create_new_chat(payload, request:Request):
    email_id = get_jwt_email(decoded_token=payload)
    
    try:
        chat_id = await generate_chat_id(email_id=email_id)
        
        chat_name = await default_chat_name(email_id=email_id)
        chats = Chats(
            chat_id=chat_id,
            email_ID=email_id,
            chat_name=chat_name
        )
        
        await chats.insert()

        return chat_id
    
    except HTTPException as http_exc:
        init_logger(message=f"Error while creating New chat: {str(http_exc)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while creating new chat"
        )

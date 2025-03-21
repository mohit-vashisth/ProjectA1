from backend.utils.logger import init_logger
from backend.schemas.chat_schema import Chats
from backend.security.jwt_data_extract import get_jwt_email
from backend.security.create_n_verify_chat_id import generate_chat_id, default_chat_name

from fastapi import HTTPException, status, Request

async def create_new_chat(payload, request:Request):
    
    try:
        init_logger(message=f"creating new chat", request=request)
        email_id = get_jwt_email(decoded_token=payload)
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
        init_logger(message=f"Error while creating New chat: {str(http_exc)}", level="error", request=request)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while creating new chat"
        )

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse

from backend.core import config
from backend.schemas.chat_schema import Chats
from backend.security.jwt_data_extract import get_jwt_email
from backend.security.token_verification import verify_and_refresh_token
from backend.utils.logger import init_logger


delete_chat_route = APIRouter()

@delete_chat_route.post(path=f"{config.VITE_STORAGE_FILES_EP}/delete-chats", status_code=status.HTTP_200_OK)
async def delete_chat(chat_id, request: Request):
    try:
        # payload = await verify_and_refresh_token(request=request)
        # email_id = get_jwt_email(decoded_token=payload)
        email_id = "naveenmuwal2052003@gmail.com"

        chat = Chats.find_one({"chat_id":chat_id, "email_id": email_id})
        if chat is None:
            init_logger(message=f"No chat found with chat_id: {chat_id}", level="error")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No chat found.")
        await chat.delete()
        return JSONResponse(
            content={
                "message": "Chat deleted successfully."
            }
        )
    
    except Exception as e:
        init_logger(message=f"Unexpected error while renaming chat: {str(e)}", level="Warning")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while renaming chat")    

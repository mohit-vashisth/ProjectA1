from backend.core import config
from backend.utils.logger import init_logger
from backend.schemas.chat_schema import Chats

from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Request, status


delete_chat_route = APIRouter()

@delete_chat_route.post(path=f"{config.VITE_STORAGE_FILES_EP}/delete-chats", status_code=status.HTTP_200_OK)
async def delete_chat(chat_id, request: Request):

    # payload = await verify_and_refresh_token(request=request)
    # email_id = get_jwt_email(decoded_token=payload)
    email_id = "naveenmuwal2052003@gmail.com"

    chat = Chats.find_one({"chat_id":chat_id, "email_id": email_id})

    if chat is None:
        init_logger(message=f"No chat found with chat_id: {chat_id}", level="warning", request=request)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No chat found.")
    
    await chat.delete()

    return JSONResponse(
        content={
            "message": "Chat deleted successfully."
        }
    )
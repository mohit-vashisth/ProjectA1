from backend.core import config
from backend.utils.logger import init_logger
from backend.schemas.chat_schema import Chats, RenameChat
from backend.security.jwt_data_extract import get_jwt_email
from backend.security.token_verification import verify_and_refresh_token

from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Request, status


rename_chat_route = APIRouter()
@rename_chat_route.post(path=config.RENAME_EP, status_code=status.HTTP_200_OK)
async def rename_chat(rename: RenameChat, request: Request):

    payload = await verify_and_refresh_token(request=request)
    email_id = get_jwt_email(decoded_token=payload)
    chat = await Chats.find_one({"chat_id":rename.chat_id, "email_ID": email_id})
    
    if chat is None:
        init_logger(message=f"No chat found with chat_id: {rename.chat_id}", level="warning", request=request)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No chat found.")
    
    init_logger(message=f"Chat found with chat_id: {rename.chat_id}", request=request)
    await chat.update({"$set":{"chat_name": rename.new_chat_name}})
    init_logger(message=f"Chat name updated to: {rename.new_chat_name}", request=request)

    return JSONResponse(
        content={
            "message": "Chat renamed successfully",
            "chat_id": rename.chat_id
        }
    )
from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status
from fastapi.responses import JSONResponse

from backend.core import config
from backend.schemas.chat_schema import Chats, RenameChat
from backend.security.jwt_data_extract import get_jwt_email
from backend.security.token_verification import verify_and_refresh_token
from backend.utils.logger import init_logger


rename_chat_route = APIRouter()
@rename_chat_route.post(path=config.VITE_RENAME_EP, status_code=status.HTTP_200_OK)
async def rename_chat(rename: RenameChat, request: Request):
    try:
        payload = await verify_and_refresh_token(request=request)
        email_id = get_jwt_email(decoded_token=payload)
        chat = await Chats.find_one({"chat_id":rename.chat_id, "email_ID": email_id})
        if chat is None:
            init_logger(message=f"No chat found with chat_id: {rename.chat_id}", level="error")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No chat found.")
        
        init_logger(message=f"Chat found with chat_id: {rename.chat_id}")
        await chat.update({"$set":{"chat_name": rename.new_chat_name}})
        init_logger(message=f"Chat name updated to: {rename.new_chat_name}")

        return JSONResponse(
            content={
                "message": "Chat renamed successfully",
                "chat_id": rename.chat_id
            }
        )

    except Exception as e:
        init_logger(message=f"Unexpected error while renaming chat: {str(e)}", level="Warning")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while renaming chat")
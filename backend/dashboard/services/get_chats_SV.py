from backend.core import config
from backend.utils.logger import init_logger
from backend.schemas.chat_schema import Chats
from backend.security.jwt_data_extract import get_jwt_email
from backend.security.token_verification import verify_and_refresh_token

from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, status



storage_file_route = APIRouter()

@storage_file_route.post(path=config.VITE_GET_CHATS_FILES_EP, status_code=status.HTTP_200_OK)
async def storage_files(request:Request):

    payload = await verify_and_refresh_token(request=request)
    email_id = get_jwt_email(decoded_token=payload)
    chats = await Chats.find({"email_ID": email_id}).to_list()

    if len(chats) == 0:
        init_logger(message=f"No chats found for user: {email_id} : {len(chats)}", level="warning", request=request)
        return JSONResponse(
            content = {"message": "Currently there are no chats for user."},
            status_code= status.HTTP_404_NOT_FOUND
        )

    chat_list = [{"chat_id": chat.chat_id, "chat_name": chat.chat_name} for chat in chats]
    init_logger(message=f"chats found for user: {email_id} : {len(chats)}", request=request)

    return JSONResponse(
        content={
            "chat_list": chat_list
        }
    )
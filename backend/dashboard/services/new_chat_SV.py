from backend.core import config
from backend.utils.logger import init_logger
from backend.auth.new_chats import create_new_chat
from backend.security.token_verification import verify_and_refresh_token

from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, status

new_chat_route = APIRouter()
@new_chat_route.get(path=config.VITE_NEW_CHAT_EP, status_code=status.HTTP_200_OK)
async def new_chat(request: Request):
    
    init_logger(message=f"method :{request.method} | url:{request.url} | cookies: {request.cookies}", request=request)
    
    payload = await verify_and_refresh_token(request=request)

    chat_id = create_new_chat(payload=payload, request=request)

    return JSONResponse(
        content={
            "message": "New chat created successfully.",
            "session_id": chat_id
        }
    )

from fastapi import APIRouter, HTTPException, status
from core import config

new_chat_route = APIRouter()
@new_chat_route.get(path=config.VITE_NEW_CHAT_EP, status_code=status.HTTP_202_ACCEPTED)
def new_chat_service():
    pass
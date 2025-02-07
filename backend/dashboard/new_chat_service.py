from fastapi import APIRouter, HTTPException, status
from config import env_variables

new_chat_route = APIRouter()
@new_chat_route.get(env_variables("VITE_NEW_CHAT_EP"), status_code=status.HTTP_202_ACCEPTED)
def new_chat_service():
    pass
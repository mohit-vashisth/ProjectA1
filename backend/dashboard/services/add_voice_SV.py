from fastapi import APIRouter, HTTPException, Request, status
from backend.core import config
from backend.utils.logger import init_logger

user_voice_route = APIRouter()
@user_voice_route.post(path=config.VITE_USER_VOICE_ADD_EP, status_code=status.HTTP_200_OK)
def user_voice(request: Request):
    pass
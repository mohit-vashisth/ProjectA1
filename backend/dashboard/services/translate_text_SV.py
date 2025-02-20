from fastapi import APIRouter, HTTPException, status
from core import config
from ml_models.language_detect import language_check

translate_route = APIRouter()

@translate_route.post(config.VITE_TRANSLATE_SPEECH_EP, status_code=status.HTTP_200_OK)
def translate():
    pass
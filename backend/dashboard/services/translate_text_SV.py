from fastapi import APIRouter, HTTPException, Request, Response, status
from backend.core import config
from backend.schemas.lang_trans_schema import Language_request
from backend.utils.logger import init_logger
from backend.security.token_verification import verify_and_refresh_token


translate_route = APIRouter()

@translate_route.post(config.VITE_TRANSLATE_SPEECH_EP, status_code=status.HTTP_200_OK)
async def translate(request: Language_request, req: Request):
    init_logger(message=f"text: {request.text} | destination: {request.dest}")
from backend.core import config
from backend.utils.logger import init_logger
from backend.schemas.lang_trans_schema import Language_request

from fastapi import APIRouter, Request, status

translate_route = APIRouter()

@translate_route.post(config.VITE_TRANSLATE_SPEECH_EP, status_code=status.HTTP_200_OK)
async def translate(req: Language_request, request: Request):
    init_logger(message=f"text: {req.text} | destination: {req.dest}", request=request)
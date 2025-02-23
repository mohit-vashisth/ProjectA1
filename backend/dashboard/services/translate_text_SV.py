from fastapi import APIRouter, HTTPException, status
from backend.core import config
from ml_models.language_detect.language_check import detect_lang
from backend.schemas.lang_trans_schema import Language_request


translate_route = APIRouter()

@translate_route.post(config.VITE_TRANSLATE_SPEECH_EP, status_code=status.HTTP_200_OK)
def translate(request: Language_request):
    if request.text is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Text not found."
        )
    detect_lang(lang_req=request)
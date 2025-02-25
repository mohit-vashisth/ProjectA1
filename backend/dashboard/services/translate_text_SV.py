from fastapi import APIRouter, HTTPException, status
from backend.core import config
from backend.schemas.lang_trans_schema import Language_request
from ml_models.language_detect.language_check import text_lang_detect


translate_route = APIRouter()

@translate_route.post(config.VITE_TRANSLATE_SPEECH_EP, status_code=status.HTTP_200_OK)
def translate(request: Language_request):
    if request.text is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Text not found."
        )
    text_lang_detect(request)
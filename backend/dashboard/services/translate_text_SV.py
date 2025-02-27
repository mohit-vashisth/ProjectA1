from pydoc import text
import stat
from webbrowser import get
from colorama import init
from fastapi import APIRouter, HTTPException, status
from backend.core import config
from backend.schemas.lang_trans_schema import Language_request
from backend.utils.logger import init_logger
from ml_models.text_to_text_translate.models.google_trans_model import google_translate


translate_route = APIRouter()

@translate_route.post(config.VITE_TRANSLATE_SPEECH_EP, status_code=status.HTTP_200_OK)
def translate(request: Language_request):
    translated_text = google_translate(request)
    init_logger(message=f"translated response: {translated_text}")

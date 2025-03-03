from fastapi import APIRouter, HTTPException, status
from backend.core import config
from backend.schemas.lang_trans_schema import Language_request
from backend.utils.logger import init_logger
from ml_models.text_to_text_translate.model_controller import translate_req_handler


translate_route = APIRouter()

@translate_route.post(config.VITE_TRANSLATE_SPEECH_EP, status_code=status.HTTP_200_OK)
def translate(request: Language_request):
    try:
        init_logger(message=f"text: {request.text} | destination: {request.dest}", level="critical")
        if not request.text:
            init_logger(message="Text is too small or not found", level="error")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is too small or not found"
            )
        try:
            translated_text_res = translate_req_handler(request=request)
            init_logger(message=f"translated_text_res: {translated_text_res}")
        except RuntimeError as rnn_error:
            pass

        return {
            "text": translated_text_res
        }

    except HTTPException as http_exp:
        init_logger(message=f"Unexpected error during translation: {str(http_exp)}", level="error")
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unexpected error during translation"
        )
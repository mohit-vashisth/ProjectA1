from fastapi import APIRouter, HTTPException, Request, Response, status
from backend.core import config
from backend.schemas.lang_trans_schema import Language_request
from backend.utils.logger import init_logger
from ml_models.text_to_text_translate.model_controller import translate_req_handler
from backend.security.token_verification import verify_n_refresh_token


translate_route = APIRouter()

@translate_route.post(config.VITE_TRANSLATE_SPEECH_EP, status_code=status.HTTP_200_OK)
async def translate(request: Language_request, req: Request):
    try:
        init_logger(message=f"text: {request.text} | destination: {request.dest}")
        await verify_n_refresh_token(request=req)
        
        translated_text_res = translate_req_handler(request=request)
        
        init_logger(message=f"translated_text_res: {translated_text_res}")

        return { "text": translated_text_res }

    except Exception as e:
        init_logger(message=f"Unexpected error during translation: {str(e)}", level="error")
        HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
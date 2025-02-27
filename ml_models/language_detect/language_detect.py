from colorama import init
from fasttext import load_model
from fastapi import HTTPException, status
from backend.core import config
from backend.schemas.lang_trans_schema import Language_request, Language_response
from backend.utils.logger import init_logger

def language_detect(request: Language_request):
    init_logger(message=f"User Text: {request.text}", level="error")
    try:
        model = load_model(config.MODEL_PATH)
        predictions = model.predict(text=request.text, k=1)
        if not predictions or not predictions[0]:
            init_logger(message=f"User Text: {request.text}", level="error")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail = "Text is too small or not found"
            )
        
        language_code = predictions[0][0].replace("__label__", "")
        confidence = predictions[1][0]
        init_logger(message=f"lang_code:{language_code} | accuracy: {confidence * 100:.2f}%", level="error")
    
        return Language_response(
            text=request.text,
            dest=request.dest,
            src=language_code
        )
    

    except HTTPException as e:
        init_logger(message=f"http {str(e)}", level="error")
        raise e
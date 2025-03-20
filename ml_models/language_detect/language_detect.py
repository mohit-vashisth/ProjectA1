from fastapi import HTTPException, status
from backend.core import config
from backend.utils.logger import init_logger
from ml_models.schemas.lang_trans_schema import Language_request, Language_response
import fasttext
import re
import os

try:
    if not os.path.exists(config.MODEL_PATH):
        raise FileNotFoundError(f"FastText model not found at {config.MODEL_PATH}")
    
    detect_model = fasttext.load_model(config.MODEL_PATH)

except Exception as model_load_err:
    init_logger(message=f"Failed to load FastText model: {str(model_load_err)}", level="error")
    detect_model = None  # Prevent crashes


def detect_language(request: Language_request) -> Language_response:
    try:
        init_logger(message=f"user text for translation: {request.text}")
        
        if not detect_model:
            init_logger(message="Unable to Load Model", level="warning")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to Load Model."
            )
        
        text = re.sub(r"[^a-zA-Z\u0900-\u097F\s]", "", request.text).strip()

        if not text:
            init_logger(message="Text is too small or empty.", level="warning")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is too small or empty."
            )
        
        try:
            predictions = detect_model.predict(text=text, k=1)
        except Exception as fasttext_err:
            init_logger(message=f"FastText prediction error: {str(fasttext_err)}", level="error")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error occurred while detecting language."
            )

        if not predictions or not predictions[0]:
            init_logger(message="Language detection failed.", level="warning")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not detect language."
            )

        detected_lang = predictions[0][0].replace("__label__", "")
        confidence = predictions[1][0]

        if confidence >= 0.72:
            src_lang = detected_lang
        else:
            src_lang = "en"

        init_logger(message=f"Detected Language: {detected_lang} | Confidence: {confidence}")

        return Language_response(text=request.text, dest=request.dest, src=src_lang)

    except HTTPException as http_exp:
        init_logger(message=f"HTTP Exception: {http_exp.detail}", level="error")
        raise http_exp

    except Exception as e:
        init_logger(message=f"Unexpected error: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while detecting language."
        )

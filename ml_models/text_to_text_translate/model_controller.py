from fastapi import status, HTTPException
from ml_models.schemas.lang_trans_schema import Language_request
from backend.utils.logger import init_logger
from ml_models.language_detect.language_detect import detect_language
from ml_models.text_to_text_translate.models.google_trans_model import google_Trans_transltor


def translate_req_handler(request: Language_request) -> str:
    try:
        response = detect_language(request=request)

        if not response or not response.src:
            init_logger(message="Language detection failed. Response is invalid.", level="error")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Failed to detect source language."
            )
        
        init_logger(message=f"Request handler received response from detect_language: {response}")

        return google_Trans_transltor(response=response)

    except HTTPException as http_err:
        init_logger(message=f"HTTP Exception in translate_req_handler: {http_err.detail}", level="error")
        raise http_err

    except Exception as e:
        init_logger(message=f"Unexpected error in translate_req_handler: {str(e)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred in the translation process."
        )
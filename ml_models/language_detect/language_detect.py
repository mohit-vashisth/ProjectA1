from fastapi import HTTPException, status
from backend.core import config
from backend.utils.logger import init_logger
from backend.schemas.lang_trans_schema import Language_request, Language_response
from fasttext import load_model

def detect_language(request: Language_request) -> Language_response:
    try:
        detect_model = load_model(config.MODEL_PATH)

        predictions = detect_model.predict(text=request.text, k=1)

        if not predictions or not predictions[0]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text is too small or empty"
            )
        language_code = predictions[0][0].replace("__label__", "")

        return Language_response(text=request.text, dest=request.dest, src=language_code)
    except ValueError as val_exp:
        init_logger(message="Text is too smal or empty.")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Text is too smal or empty." 
        )
    except HTTPException as http_exp:
        init_logger(message="Unable to proceed your request due to large number of requests")
        raise http_exp
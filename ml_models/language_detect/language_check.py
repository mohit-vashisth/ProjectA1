from fasttext import load_model
from fastapi import HTTPException, status
from backend.core import config
from backend.schemas.lang_trans_schema import Language_request
from backend.utils.logger import init_logger



def text_lang_detect(lang_req: Language_request):
    try:
        model = load_model(config.MODEL_PATH)
    
        if model is None or not lang_req.text or not lang_req.text.strip():
            init_logger(message="could not able to load model", level="warning")
            raise RuntimeError("Unable to Load Model")
        
        predictions = model.predict(lang_req.text, k=1)
        
        if not predictions or not predictions[0]:
            init_logger(message="Text Is too small or not present.", level="warning")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text Is too small or not present."
            )
        
        detected_lang = predictions[0][0]
        confidence = predictions[1][0]

        init_logger(message=f"Detected Language: {detected_lang} | Accuracy: {confidence}")
        return detected_lang, confidence

    except RuntimeError as run_err:
        init_logger(message=f"Unable to Load Model: {str(run_err)}", level="error")
        raise RuntimeError(f"Unable to Load Model: {str(run_err)}")
    except Exception as exp_err:
        init_logger(message=f"Internal Server Error: {str(exp_err)}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )
import fasttext
from fastapi import HTTPException, status
from backend.core import config
from backend.schemas.lang_trans_schema import Language_request
from backend.utils.logger import init_logger

try:
    model = fasttext.load_model(path=config.MODEL_PATH)
    init_logger(message="model loaded")
except HTTPException as http_exp:
        init_logger(message=f"Error Loading Model {http_exp}", level="error")
        raise http_exp

def text_lang_detect(lang_req: Language_request):
    try:
        predictions = model.predict(lang_req.text, k=1, threshold=7.5)
        language = predictions[0]
        assert language
        language = language[0]
        confidence = predictions[1][0]
        init_logger(message=f"Detected Language: {language} | Accuracy: {confidence}")
        

    except HTTPException as http_exp:
        init_logger(message=f"Error Detecting Language {http_exp}", level="error")
        raise http_exp
    except Exception as e:
        init_logger(message=f"model: {e}", level="error")
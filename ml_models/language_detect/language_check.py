import fasttext
from fastapi import HTTPException, status
from backend.core import config
from backend.schemas.lang_trans_schema import Language_request
from backend.utils.logger import init_logger

def text_lang_detect():
    try:
        model = fasttext.load_model(path=config.MODEL_PATH)
        if model:
            init_logger(message="model: {model}")

    except HTTPException as http_exp:
        init_logger(message="model: {model}", level="error")
        raise http_exp
    except Exception as e:
        init_logger(message="model: {model}", level="error")
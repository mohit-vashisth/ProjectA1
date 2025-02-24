import fasttext
from fastapi import HTTPException, status
from backend.core import config
from backend.schemas.lang_trans_schema import Language_request

MODEL_PATH = "../ml_models/language_detect/model/lid.176.ftz"
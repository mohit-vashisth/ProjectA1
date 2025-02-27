from backend.schemas.lang_trans_schema import Language_request
from backend.utils.logger import init_logger
from ml_models.language_detect.language_detect import detect_language
from ml_models.text_to_text_translate.models.google_trans_model import google_Trans_transltor


def translate_req_handler(request: Language_request) -> str:
    response = detect_language(request=request)
    init_logger(message=f" req_handler get response from detect_Language{response}")
    return google_Trans_transltor(response=response)


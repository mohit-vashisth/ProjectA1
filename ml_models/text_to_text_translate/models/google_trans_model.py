from backend.schemas.lang_trans_schema import Language_request, Language_response
from backend.utils.logger import init_logger
from ml_models.language_detect.language_detect import language_detect
from googletrans import Translator

def google_translate(lang_req: Language_request):
    response = language_detect(request=lang_req)

    translator = Translator(raise_exception=True)
    translated_text =  translator.translate(response.text, response.dest, response.src)
    init_logger(message=f"Translated_Text: {translated_text}", level="critical")
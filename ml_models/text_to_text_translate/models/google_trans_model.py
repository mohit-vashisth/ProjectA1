from googletrans import Translator

from backend.schemas.lang_trans_schema import Language_response
from backend.utils.logger import init_logger

def google_Trans_transltor(response: Language_response):
    try:
        translator = Translator()
        translated_text = translator.translate(text=response.text, dest=response.dest, src=response.src).text
        init_logger(message=f"final text: {translated_text}")
        return translated_text
    except Exception as e:
        init_logger(message=f"an error occured: {str(e)}", level="error")
        raise RuntimeError("Unable to translate")
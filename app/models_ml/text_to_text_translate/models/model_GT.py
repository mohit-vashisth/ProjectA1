from deep_translator import GoogleTranslator

from app.schemas.language_translate import LanguageResponse
from app.utils.logger import init_logger


def google_Trans_transltor(response: LanguageResponse):
    try:
        translated_text = GoogleTranslator(
            source="auto",
            target=response.dest
        ).translate(response.text)

        init_logger(message=f"final text: {translated_text}")
        return translated_text

    except Exception as e:
        init_logger(message=f"an error occurred: {str(e)}", level="error")
        raise RuntimeError("Unable to translate")
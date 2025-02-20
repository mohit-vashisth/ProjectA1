import fasttext
from schemas.lang_trans_schema import Language_request

def translate_text(lang: Lang) -> Lang:
    model = fasttext.load_model("lid.176.ftz")
    Language_request.language
    Language_request.text
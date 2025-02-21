import fasttext
from backend.schemas.lang_trans_schema import Language_request

def translate_text(lang_req: Language_request):
    """ -> Language_request"""
    model = fasttext.load_model("./model/lid.176.ftz")
    
    print(lang_req.text)
    print(lang_req.language)
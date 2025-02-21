import fasttext
from fastapi import HTTPException, status
from backend.core import config
from backend.schemas.lang_trans_schema import Language_request

model = fasttext.load_model("../ml_models/language_detect/model/lid.176.ftz")
try:
    model = fasttext.load_model(model)
except Exception as e:
    raise RuntimeError(f"Failed to load FastText model: {str(e)}")

def detect_lang(lang_req: Language_request):
    predictions = model.predict(lang_req.text, k=1, threshold=0.75)
    label = predictions[0]
    if label:
        labels = label[0].replace("__label__","")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="text is small or not found"
        )
from pydantic import BaseModel, constr
from core import config

class Language_request(BaseModel):
    text: constr(max_length=config.LENGTH)
    language: constr(min_length=2, max_length=5)

class Language_response(BaseModel):
    text: str
    language: str
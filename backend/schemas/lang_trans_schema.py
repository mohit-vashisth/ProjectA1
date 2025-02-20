from pydantic import BaseModel, Field
from core import config

class Language_request(BaseModel):
    text: str = Field(..., max_length=config.LENGTH)
    language: str = Field(..., min_length=2, max_length=5)

class Language_response(BaseModel):
    text: str
    language: str
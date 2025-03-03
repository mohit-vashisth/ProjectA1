from pydantic import BaseModel, Field
from backend.core import config

class Language_request(BaseModel):
    text: str = Field(default=..., max_length=int(config.LENGTH))
    dest: str = Field(default=..., min_length=2, max_length=2)

class Language_response(BaseModel):
    text: str
    dest: str
    src: str
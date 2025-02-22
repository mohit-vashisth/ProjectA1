from pydantic import BaseModel, Field
from core import config

class Language_request(BaseModel):
    text: str = Field(default=..., max_length=config.LENGTH)
    language: str = Field(default=..., min_length=2, max_length=5)

class Language_response(BaseModel):
    text: str
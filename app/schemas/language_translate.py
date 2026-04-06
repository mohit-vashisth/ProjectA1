from pydantic import BaseModel, Field, field_validator
from app.core import config

from enum import Enum

class SupportedLanguages(str, Enum):
    en = "en"
    hi = "hi"

class LanguageRequest(BaseModel):
    text: str = Field(default=..., min_length=1, max_length=int(config.LENGTH))
    dest: SupportedLanguages = Field(default=..., min_length=2, max_length=2)

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, text) -> str:
        if not text.strip():
            raise ValueError("Text must not be empty.")
        return text

    @field_validator("dest")
    @classmethod
    def dest_must_not_be_empty(cls, dest) -> str:
        if not dest.strip():
            raise ValueError("Destination language must not be empty.")
        return dest

class LanguageResponse(BaseModel):
    text: str
    dest: SupportedLanguages
    src: str

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, text) -> str:
        if not text.strip():
            raise ValueError("Text must not be empty.")
        return text

    @field_validator("dest")
    @classmethod
    def dest_must_not_be_empty(cls, dest) -> str:
        if not dest.strip():
            raise ValueError("Destination language must not be empty.")
        return dest

    @field_validator("dest")
    @classmethod
    def src_must_not_be_empty(cls, src) -> str:
        if not src.strip():
            raise ValueError("Source language must not be empty.")
        return src
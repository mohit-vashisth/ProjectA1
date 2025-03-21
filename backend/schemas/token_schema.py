from backend.utils.current_time import current_time

from enum import Enum
from beanie import Document
from datetime import datetime
from pydantic import EmailStr, model_validator

class TokenType(str, Enum):
    REFRESH = "refresh"
    BLACKLIST = "blacklist"
    ACCESS = "access"

class Tokens(Document):
    email_ID: EmailStr
    token: str
    token_type: TokenType
    expires_at: datetime | None = None
    blacklisted_at: datetime | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_token(cls,values):
        token_type= values.get("token_type")

        if token_type == TokenType.REFRESH and not values.get("expires_at"):
            raise ValueError("expires_at is required for refresh token.")

        elif token_type == TokenType.BLACKLIST:
            if values.get("expires_at"):
                raise ValueError("expires_at is not required for blacklist token.")
            values["blacklisted_at"] = current_time()
            values["expires_at"] = None
        
        return values
    
    class Settings:
        name = "tokens"
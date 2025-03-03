from beanie import Document
from datetime import datetime

class RefreshToken(Document):
    email_id: str
    refresh_token: str
    expires_at: datetime

    class Settings:
        name = "refresh_tokens"
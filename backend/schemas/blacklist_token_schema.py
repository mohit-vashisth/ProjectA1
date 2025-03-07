from datetime import datetime
from beanie import Document
from pydantic import Field

from backend.utils.current_time import current_time

class BlacklistToken(Document):
    token: str
    blacklisted_at: datetime = Field(default_factory=lambda: current_time())

    class Settings:
        collection = "BlacklistToken"
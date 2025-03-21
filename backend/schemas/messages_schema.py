from backend.utils.current_time import current_time

from pydantic import Field
from beanie import Document
from datetime import datetime


class Messages(Document):
    chat_id: str
    text: str
    audio_url: str
    created_at: datetime = Field(default_factory=lambda: current_time())
    
    class Settings:
        collection = "Messages"
        indexes = [
            "chat_id",
            [("created_at", -1)]
        ]
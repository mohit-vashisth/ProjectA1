from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field, EmailStr
from backend.utils.current_time import current_time

class Chat(BaseModel):
    chat_id: str
    chat_name: str
    created_at: datetime = Field(default_factory=lambda: current_time())
    
class Chats(Document):
    email_ID: EmailStr
    chat: list[Chat]

    class Settings:
        collection = "Chats"
        indexes = [
            "chat_id",
            "email_ID",
            [("created_at", -1)]
        ]

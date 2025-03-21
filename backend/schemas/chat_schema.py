from backend.utils.current_time import current_time

from beanie import Document
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

    
class Chats(Document):
    chat_id: str
    email_ID: EmailStr
    chat_name: str
    created_at: datetime = Field(default_factory=lambda: current_time())

    class Settings:
        collection = "Chats"
        indexes = [
            "chat_id",
            "email_ID",
            [("created_at", -1)]
        ]

class RenameChat(BaseModel):
    chat_id: str
    new_chat_name: str
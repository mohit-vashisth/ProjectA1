from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field, EmailStr
from backend.utils.current_time import current_time

    
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
from datetime import datetime
from beanie import Document
from pydantic import Field, EmailStr
from backend.utils.current_time import current_time

class Chats(Document):
    chat_id: str
    timestamp: datetime = Field(default_factory=lambda: current_time())
    email_ID: EmailStr
    text: str
    translated_text: str

from beanie import Document
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    sender_id: str
    text: str
    timestamp: datetime = datetime.now()

class Chat(Document):
    participants: List[str]  # List of user IDs
    messages: List[Message] = []
    created_at: datetime = datetime.now()

    class Settings:
        collection_name = "chats"  # Name of the MongoDB collection

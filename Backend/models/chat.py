from beanie import Document
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    TEXT = "text"
    VOICE = "voice"
    TRANSLATED_VOICE = "translated_voice"

class VoiceData(BaseModel):
    audio_path: str
    duration: float
    sample_rate: int = 16000
    voice_embedding: Optional[List[float]] = None  # For voice cloning features

class Message(BaseModel):
    sender_id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1, max_length=5000)
    message_type: MessageType
    timestamp: datetime = Field(default_factory=datetime.now)
    voice_data: Optional[VoiceData] = None
    target_language: Optional[str] = None  # For translation features
    
    @model_validator(mode='before')
    def validate_message(cls, data):
        if not data.get('text', '').strip():
            raise ValueError('Message text cannot be empty')
        
        # Validate voice data presence for voice messages
        if data.get('message_type') in [MessageType.VOICE, MessageType.TRANSLATED_VOICE]:
            if not data.get('voice_data'):
                raise ValueError('Voice data required for voice messages')
                
        data['text'] = data.get('text', '').strip()
        return data

class Chat(Document):
    chat_id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    user_id: str
    user_voice_profile: Optional[str] = None  # Path to user's voice profile
    voice_characteristics: Optional[dict] = None  # Store voice characteristics
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    class Settings:
        name = "voice_chats"
        indexes = [
            "user_id",
            "created_at",
            "chat_id"
        ]
    
    async def add_message(self, message: Message) -> None:
        """Add a new message to the chat"""
        self.messages.append(message)
        self.last_updated = datetime.now()
        await self.save()
    
    async def update_voice_profile(self, profile_path: str, characteristics: dict) -> None:
        """Update user's voice profile"""
        self.user_voice_profile = profile_path
        self.voice_characteristics = characteristics
        await self.save()

# Database initialization function
async def init_db(db_url: str, db_name: str):
    """Initialize database connection"""
    client = AsyncIOMotorClient(db_url)
    await init_beanie(database=client[db_name], document_models=[Chat])


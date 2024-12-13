from beanie import Document
from pydantic import Field
from datetime import datetime, timedelta
from typing import Optional

class Session(Document):
    user_id: str
    session_token: str
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(days=7)
    )
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    
    class Settings:
        name = "sessions"
        indexes = [
            "user_id",
            "session_token",
            "expires_at"
        ]
    
    async def is_valid(self) -> bool:
        return datetime.now() < self.expires_at
    
    async def update_activity(self):
        self.last_activity = datetime.now()
        await self.save()

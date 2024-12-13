from beanie import Document
from pydantic import BaseModel, Field, EmailStr, model_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"

class UserPreferences(BaseModel):
    theme: str = "light"
    language: str = "en"
    notifications_enabled: bool = True

class User(Document):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password_hash: str
    status: UserStatus = UserStatus.ACTIVE
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Settings:
        name = "users"
        indexes = [
            "email",
            "username",
            "status"
        ]
    
    @model_validator(mode='before')
    def validate_user(cls, data):
        if 'username' in data:
            data['username'] = data['username'].lower().strip()
        return data
    
    async def update_last_login(self):
        self.last_login = datetime.now()
        await self.save()

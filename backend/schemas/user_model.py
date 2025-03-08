from pydantic import BaseModel, Field, EmailStr
from beanie import Document
from datetime import datetime
from backend.utils.current_time import current_time

class UserProfile(BaseModel):
    user_name: str
    contact_number: str

class Auth(BaseModel):
    password: str

class LoginHistory(BaseModel):
    ip_address: str
    time_zone: str
    login_time: datetime


class Users(Document):
    email_ID: EmailStr
    profile: UserProfile
    auth: Auth
    is_Premium: bool = Field(default=False)
    created_at: datetime = Field(default_factory= current_time)
    updated_at: datetime = Field(default_factory= current_time)
    privacy_link: bool

    class Settings:
        collection = "Users"
        indexes = [
            "email_ID",  # Unique Index
            [("created_at", -1)] # Sorting by latest users
        ]


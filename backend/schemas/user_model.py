from datetime import datetime
from pydantic import Field, EmailStr
from beanie import Document, Indexed
from datetime import datetime, timezone

class Users(Document):
    user_name: str
    email_ID: EmailStr = Field(default=..., unique=True, index=True)  # Ensure email is unique
    password: str  # Store hashed password
    time_zone: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Timezone-aware datetime
    privacy_link: bool
    contact_number: str

    @property
    def get_id(self):
        return str(self.id)  # Using MongoDB ObjectId

    class Settings:
        collection = "Users"


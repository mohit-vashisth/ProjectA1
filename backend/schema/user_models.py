from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from beanie import Document

# whenever we create an instance date and time will be set to actual time when it will be created.
class User_signup(BaseModel):
    user_name: str = Field(..., alias="userName")
    email_ID: EmailStr = Field(..., alias="userEmail")
    password: str = Field(..., alias="userPassword")
    time_zone: str = Field(..., alias="timeZone")
    privacy_link: bool = Field(..., alias="privacyCheck")
    contact_number: str = Field(..., alias="ContactNumber")

    class config:
        extra= "ignore"


# whenever we create an instance date and time will be set to actual time when it will be created.
class User_login(BaseModel):
    email_ID: EmailStr = Field(..., alias="email")
    password: str = Field(..., alias="password")

    class config:
        extra= "ignore"


class User_db_model(Document):
    user_name: str
    email_ID: EmailStr
    password: str
    time_zone: str
    created_at: datetime = Field(default_factory=datetime.now)
    privacy_link: bool
    contact_number: str

    class settings:
        extra = "users"
        indexes = [
            "email_ID",
            [("created_at", -1)], # -1 for decending, we will get latest users on the top and oldest user at last
            "user_name"
        ]
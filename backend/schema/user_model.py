from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

# whenever we create an instance date and time will be set to actual time when it will be created.
class User_signup(BaseModel):
    user_name: str = Field(..., alias="userName")
    email_ID: EmailStr = Field(..., alias="userEmail")
    password: str = Field(..., alias="userPassword")
    signup_time: datetime = Field(default_factory=datetime.now)
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

from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

# whenever we create an instance date and time will be set to actual time when it will be created.
class User_signup(BaseModel):
    user_name: str = Field(..., alias="userName")
    email_ID: EmailStr = Field(..., alias="userEmail")
    password: str = Field(..., alias="userPassword")
    signup_time: datetime = Field(default_factory=datetime.now)
    time_zone: str = Field(..., alias="timeZone")


# whenever we create an instance date and time will be set to actual time when it will be created.
class User_login(BaseModel):
    email_ID: EmailStr = Field(..., alias="userEmail")
    password: str = Field(..., alias="userPassword")
    signup_time: datetime = Field(default_factory=datetime.now)
    time_zone: str = Field(..., alias="timeZone")

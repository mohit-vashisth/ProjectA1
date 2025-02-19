from pydantic import BaseModel, EmailStr, Field, Extra
import pytz
# whenever we create an instance date and time will be set to actual time when it will be created.
class User_signup(BaseModel):
    user_name: str = Field(..., alias="userName")
    email_ID: EmailStr = Field(..., alias="userEmail")
    password: str = Field(..., alias="userPassword")
    time_zone: str = Field(..., alias="timeZone")
    privacy_link: bool = Field(..., alias="privacyCheck")
    contact_number: str = Field(..., alias="ContactNumber")

    

    class Config:
        extra = Extra.forbid


# whenever we create an instance date and time will be set to actual time when it will be created.
class User_login(BaseModel):
    email_ID: EmailStr = Field(..., alias="email")
    password: str = Field(..., alias="password")

    class Config:
        extra = Extra.forbid
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class User_signup(BaseModel):
    user_name: str = Field(default=..., alias="userName")
    email_ID: EmailStr = Field(default=..., alias="userEmail")
    password: str = Field(default=..., alias="userPassword")
    time_zone: str = Field(default=..., alias="timeZone")
    privacy_link: bool = Field(default=..., alias="privacyCheck")
    contact_number: str = Field(default=..., alias="contactNumber")

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class User_login(BaseModel):
    email_ID: EmailStr = Field(default=..., alias="email")
    password: str = Field(default=..., alias="password")

    model_config = ConfigDict(extra="forbid", populate_by_name=True)
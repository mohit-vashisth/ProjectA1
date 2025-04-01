from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator

class UserSignup(BaseModel):
    user_name: str = Field(default=..., min_length=1, alias="userName")
    email_ID: EmailStr = Field(default=..., alias="userEmail")
    password: str = Field(default=..., min_length=6, alias="userPassword")
    time_zone: str = Field(default=..., min_length=1, alias="timeZone")
    privacy_link: bool = Field(default=..., alias="privacyCheck")
    contact_number: str = Field(default=...,min_length=10, alias="contactNumber")

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    @field_validator("user_name")
    @classmethod
    def user_name_must_not_be_empty(cls, user_name) -> str:
        if not user_name.strip():
            raise ValueError("name must not be empty.")
        return user_name
    
    @field_validator("email_ID")
    @classmethod
    def email_must_not_be_empty(cls, email_ID) -> EmailStr:
        if not email_ID.strip():
            raise ValueError("email must not be empty.")
        return email_ID
    
    @field_validator("password")
    @classmethod
    def password_must_not_be_empty(cls, password) -> str:
        if not password.strip():
            raise ValueError("password must not be empty.")
        return password

    @field_validator("time_zone")
    @classmethod
    def time_zone_must_not_be_empty(cls, time_zone) -> str:
        if not time_zone.strip():
            raise ValueError("time zone must not be empty.")
        return time_zone
    
    @field_validator("privacy_link")
    @classmethod
    def privacy_link_must_not_be_empty(cls, privacy_link) -> bool:
        if not privacy_link:
            raise ValueError("privacy must be true.")
        return privacy_link
    
    @field_validator("contact_number")
    @classmethod
    def contact_number_must_not_be_empty(cls, contact_number) -> str:
        if not contact_number.strip():
            raise ValueError("contact number must not be empty.")
        return contact_number


class UserLogin(BaseModel):
    email_ID: EmailStr = Field(default=..., alias="email")
    password: str = Field(default=..., min_length=6, alias="password")
    time_zone: str = Field(default=..., min_length=1, alias="timeZone")

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    @field_validator("email_ID")
    @classmethod
    def email_must_not_be_empty(cls, email_ID) -> EmailStr:
        if not email_ID.strip():
            raise ValueError("email id must not be empty.")
        return email_ID
    
    @field_validator("password")
    @classmethod
    def password_must_not_be_empty(cls, password) -> str:
        if not password.strip():
            raise ValueError("password must not be empty.")
        return password
    
    @field_validator("time_zone")
    @classmethod
    def time_zone_must_not_be_empty(cls, time_zone) -> str:
        if not time_zone.strip():
            raise ValueError("time zone must not be empty.")
        return time_zone
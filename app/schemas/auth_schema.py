from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# REGISTER
class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)
    full_name: str = Field(min_length=3, max_length=100)
    education_level: str = Field(max_length=20)


class RegisterResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    education_level: str
    created_at: datetime


# LOGIN
class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:

        if " " in value:
            raise ValueError("Username tidak boleh mengandung spasi")

        return value


class LoginUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    full_name: str


class LoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    token_type: str
    user: LoginUserResponse

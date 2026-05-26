from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    education_level: str
    created_at: datetime


class UpdateProfileRequest(BaseModel):
    full_name: str
    education_level: str

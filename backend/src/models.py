from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    fullName: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user response (without password)"""
    id: str
    fullName: str
    email: str
    createdAt: datetime

    class Config:
        from_attributes = True


class UserInDB(BaseModel):
    """Schema for user stored in database"""
    fullName: str
    email: str
    password: str  # This will be hashed
    createdAt: datetime = Field(default_factory=datetime.utcnow)

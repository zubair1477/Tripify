from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, List
from datetime import datetime


# User Models
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


# Quiz Models
class QuizAnswers(BaseModel):
    """Schema for quiz answers submission"""
    userId: str
    answers: Dict[int, int]  # Question index -> Option index


class MoodScores(BaseModel):
    """Schema for mood calculation results"""
    energetic: float
    calm: float
    introspective: float
    adventurous: float


class MoodResult(BaseModel):
    """Schema for mood calculation response"""
    userId: str
    moodScores: MoodScores
    dominantMood: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)

# schemas.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=150)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=150)


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    age: Optional[int] = None
    created_at: Optional[datetime] = None